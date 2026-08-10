# 🚩Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets and double are HTML encoded and single quotes are escaped.
To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.


### 🔍 분석 및 공격 과정
1. 검색 내용이 javascript 내에 포함되고 있는  `javascript context XSS`로 파악.
```html
<script>
  var searchTerms = 'exam';
  document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
+ 저기에 img 태그를 사용해 트래킹서버로 보내고 있는데 이는 img태그의 src 속성의 특징때문. src로 get요청을 보냄.
```
2. `'`에 대해 escape 처리를 하고 있고 `<`, `>`, `"` 는 HTML 인코딩을 하고 있음.
3. 그러나 backslash에 대한 처리는 없음. `입력을 exam\'` 로 준다면 `'`를 escape하기 위해 `\`를 하나 달게 되고 결과는 `exam\\'`가 됨. 즉 escape처리를 위한 backslash 자체가 escape 되어 끝에 `'`는 생존하게 됨.
4. 또한 주석문인 `//` 에 대한 처리도 없음. 그렇다면 3번과 결합하여 `exam\'+alert()//` 로 페이로드 완성.


### 💡 취약점 원리
  블랙리스팅을 통한 XSS방어의 문제점이였음.
