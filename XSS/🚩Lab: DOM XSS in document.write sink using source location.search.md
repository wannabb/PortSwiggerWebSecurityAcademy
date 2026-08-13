# 🚩Lab: DOM XSS in document.write sink using source location.search


This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality. 
It uses the JavaScript document.write function, which writes data out to the page. 
The document.write function is called with data from location.search, which you can control using the website URL.
To solve this lab, perform a cross-site scripting attack that calls the alert function.


### 🔍 분석 및 공격 과정
1. 서치 쿼리를 트래킹하는 스크립트는 다음과 같다.
```html
<script>
function trackSearch(query){
  document.write('<img src="/resources/images.tacker.gif?searchTerms='+query+'">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query){
  trackSearch(query);
}
</script>
```
2. `location.search`로 `search`의 value를 받아 트래킹서버로 img태그의 src의 특성을 이용해 get요청으로 보내며 <img> 태그를 write 한다.
3. 중요한 점은 `search`의 값을 별 다른 검증 없이 `document.write` 한다는 점.
```html " onload="alert(1) ```
4. 위와 같은 페이로드를 작성하면 `"`로 src를 탈출하고 `onload` 핸들러를 추가하고 alert()를 발생시킬 수 있다. solve


### 💡 취약점 원리
 source를 별다른 검증없이 sink로 보내는 경우 발생할 수 있는 DOM XSS 
