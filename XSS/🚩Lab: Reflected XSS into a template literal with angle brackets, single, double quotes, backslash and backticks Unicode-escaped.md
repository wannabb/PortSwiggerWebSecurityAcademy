# 🚩Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality. 
The reflection occurs inside a template string with angle brackets, single, and double quotes HTML encoded, and backticks escaped.
To solve this lab, perform a cross-site scripting attack that calls the alert function inside the template string.

### 🔍 분석 및 공격 과정
1. 임의의 검색값 `exam`을 검색해보니 돌려주는 응답에 다음과 같은 스크립트가 있었다.
```html
<script>
 var message = `0 search results for 'exam'`;
 document.getElementById('searchMessage').innerText = message;
</script>                 
```
2. message는 템플릿 리터럴이다. 따라서 `${값}`을 사용할 수 있다.
3. 검색 값으로써 `${alert()}`를 주면 간단히 solve

### 💡 취약점 원리
  템플릿 리터럴을 사용하는데 정작 $나 {, }는 escape하지 않았다.
