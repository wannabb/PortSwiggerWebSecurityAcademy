# 🚩Lab: 2FA simple bypass

```text
This lab's two-factor authentication can be bypassed.
You have already obtained a valid username and password, but do not have access to the user's 2FA verification code.
To solve the lab, access Carlos's account page
Your valid account = wiener:peter, carlos:montoya
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
2. 이메일로 인증코드가 전송이된다.
3. 혹시나 1차인증후에 바로 로그인 상태로 설정되는 결함이 있는지 확인하기 위해 /login 페이지에서 바로 루트 페이지로 이동해버린다.
4. 2차 인증이 우회되고 성공적으로 로그인된다.
5. carlos계정도 마찬가지로 2차 인증이 우회된다. solve
                        
### 💡 취약점 원리
 1차 인증이후 이미 로그인 된 것으로 처리하며 세션을 발급하여 2차인증이 사실상 무의미한 논리적 결함이 있었다. 1차인증후 발급되는 세션은 2차 인증 대기 상태로 처리되는 세션이여야만 한다.
