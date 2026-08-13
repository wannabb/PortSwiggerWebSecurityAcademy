# 🚩Lab: DOM XSS in innerHTML sink using source `location.search`

This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. 
It uses an `innerHTML` assignment, which changes the HTML contents of a div element, using data from `location.search`.
To solve this lab, perform a cross-site scripting attack that calls the alert function.

### 🔍 분석 및 공격 과정
1. sink가 존재하는 스크립트는 다음과 같다.
```html
<script>
   function doSearchQuery(query) {
   document.getElementById('searchMessage').innerHTML = query;
   }
   var query = (new URLSearchParams(window.location.search)).get('search');
   if(query) {
   doSearchQuery(query);
   }
</script>
```
2. 단순하게 `search`의 값을 쿼리스트링으로 부터 받아와서 `innerHTML`에 쓰고 있다.
3. `<img src=1 onerror=alert()>`를 search의 값으로 주면 solve
                        
### 💡 취약점 원리
 source=location.search, sink=innerHTML
