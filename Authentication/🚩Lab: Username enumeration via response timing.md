# 🚩Lab: Username enumeration via response timing

```text
This lab is vulnerable to username enumeration using its response times.
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Your credentials: wiener:peter
```

### 🔍 분석 및 공격 과정
1. `wiener:임의의 틀린패스워드` 로 로그인.
2. username이 틀리나 비밀번호가 틀리나 비슷한 응답을 돌려줌.
3. 무차별 대입 방어는 없으니 인트루더로 보내 username에 대해 대입 공격 시도. 이때 비밀번호는 충분히 긴 비밀번호로 설정. username이 유효할시 비밀번호를 비교할텐데 비밀번호가 길면 이 응답시간 차이를 더 명확하게 구별 가능할 것이라는 기대
4. 일정 횟수 이상 시도 실패하면 차단 당함..
5. `X-Forwarded-For` 의 값도 요청마다 변경하도록 설정.
6. 눈에 띄게 응답이 긴 username이 있음.
7. 해당 username을 고정시키고 아까와 같이 X-Forwarded-For의 값은 변경시켜가며 password를 bruteforce -> solve


 

### 💡 취약점 원리
 X-Forwarded-For 헤더를 리버스프록시 단에서 전적으로 신뢰하여 서버가 신뢰하는 요청 IP를 바꿔가며 bruteforce를 진행하였고 유효한 username의 경우 응답시간이 다르다는 오류를 이용하였음.  
