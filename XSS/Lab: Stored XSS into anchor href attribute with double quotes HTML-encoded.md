# 🚩Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded


This lab contains a stored cross-site scripting vulnerability in the comment functionality. 
To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

### 🔍 분석 및 공격 과정
1. 개발자 도구로 `comment` 기능을 살펴본 결과 `website`의 값으로 준 값을 `<a href='입력한 웹사이트 주소'>닉네임</a>` 로 돌려주고 있다.
2. 또한 `website` 입력 값을 검증하지 않고 있다. website의 입력에 `javascript:`스킴으로 `javascript:alert(1)`을 `href`의 value로 준다면 `<a href='javascript:alert(1)'>닉네임</a>` 가 된다.
3. solve
 
### 💡 취약점 원리
 stored XSS 취약점을 이용해, javascript를 실행시킴
