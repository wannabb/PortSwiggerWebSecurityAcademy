# 🚩Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

This lab contains a stored cross-site scripting vulnerability in the comment functionality.
To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

### 🔍 분석 및 공격 과정
1. 일단 문제를 풀기 전에 알아야 할 브라우저의 한가지 특징이 있다. 브라우저는 일단 응답의 태그와 속성들을 파싱한 후에 attribute에 입력된 value는 HTML 디코딩하는 특징이다.
2. 이를 이용하면 민감한 문자를 숨기면서 WAF등을 통과할 수 있다.
3. comment를 작성해보면 내가 입력하는 website의 주소가 <a>태그의 onclick핸들러 내부에 들어가는걸 볼 수 있음. 그렇다면 웹 주소를 `http://asc.com'+alert()+'` 로 준다면?
4. 이 경우 `'` 가 escaped되어 문자열 탈출이 불가능. 그렇다면 이번에는 `'`가 아니라 html 인코딩한 `&apos;`를 준다면?
5. `http://asc.com&apos;+alert()+&apos;` -> solve

### 💡 취약점 원리
  stored XSS. 사용자가 입력한 웹사이트의 주소가 단지 `'`만 escape처리 되어 attribute의 값으로 삽입되어 생긴 문제이다.
