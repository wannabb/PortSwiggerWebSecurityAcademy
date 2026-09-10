# 🚩Lab: Username enumeration via subtly different responses

```text
This lab is subtly vulnerable to username enumeration and password brute-force attacks.
It has an account with a predictable username and password, 

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.
```

### 🔍 분석 및 공격 과정
1. id에 대해 brute force 진행.
2. `app01`만 응답이 `Invalid username or password`로 문장끝에 `.`이 없음.
3. app01을 id에 고정 시키고 비밀번호에 대해 brute force
4. 비밀번호는 `robert` -> solve
                        
### 💡 취약점 원리
 유효한 username을 입력받았을 때 미세하게 응답의 차이가 있었으며 무차별 대입에 대한 아무 방어도 구현되어 있지 않았음.
