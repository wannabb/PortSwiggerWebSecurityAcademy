# 🚩Lab: Password reset broken logic

```text
This lab's password reset functionality is vulnerable. 
solve the lab, reset Carlos's password then log in and access his "My account" page.

Your credentials: wiener:peter
Victim's username: carlos
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인한다.
2. 여기서 살펴볼만한건 없는것 같다.
3. 로그아웃후 Forgot password기능으로 wiener의 이메일로 password 변경 링크를 발급받아온다.
4. 비밀번호 변경중 발생하는 패킷들을 살펴본다. `POST /forgot-password?temp-forgot-password-token=1ytg6u6s4thgueku1qjjk923msp81go9`
```http
temp-forgot-password-token=1ytg6u6s4thgueku1qjjk923msp81go9&username=wiener&new-password-1=1234&new-password-2=1234
```
5. body에 위와 같은 값들이 실리게 된다. `username=wiener`가 눈에 띄는데 저 값을 carlos로 바꾸면 어떻게 되는지 체크 해본다.
6. 302 코드를 반환하며 성공적으로 비밀번호가 변경되어 carlos:1234로 로그인이 가능하다 -> solve
                        
### 💡 취약점 원리
 비밀번호 변경시 발급되는 이메일의 링크 토큰이 계정에 묶이지 않았으며, 비밀번호가 변경된 후에도 유효하여 이런 취약점이 발생했다. 토큰은 변경하려는 계정에 묶여야하고 타겟 작업이 끝날시 만료되도록 설계해야한다.
