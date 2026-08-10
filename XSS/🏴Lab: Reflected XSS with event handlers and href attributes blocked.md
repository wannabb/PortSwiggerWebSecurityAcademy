# 🏴Lab: Reflected XSS with event handlers and href attributes blocked (Expert Lab)


This lab has a simple reflected XSS vulnerability. 
The site is blocking common tags but misses some SVG tags and events.
To solve the lab, perform a cross-site scripting attack that calls the alert() function.


### 🔍 분석 및 공격 과정
1. 이전 문제들과 같이 똑같은 코드로 search에서 Turbo intruder를 돌려 사용가능한 태그를 찾았다.
2. `<svg>`와 `<animate>`, `<a>` 태그가 사용 가능했다.
3. `<animate>` 태그는 `<svg>` 태그 내에서 사용 하는데 시간에 따라 태그의 값에 변화를 줄 수 있는 태그이다. 이때 `<a>`태그의 `href의 value`에도 변화를 줄 수 있다. value에 javascript: 스킴을 줘서 alert를 띄우자.
4. 다음과 같이 페이로드를 작성한다.
```html
<svg><a><animate attributeName=href values=javascript:alert(1) />click me.</a></svg>
```
5. 허나 `<svg>`태그내의 HTML의 기본 태그들의 글자는 표시되지 않는다. 이때 사용할 수 있는데 svg의 `<text>`태그.
6. `<text>`태그로 버튼을 클릭할 수 있도록 띄운다.
```html
<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>click me.</text></a></svg>
```



### 💡 취약점 원리
 마찬가지로 블랙리스팅기반으로 태그들을 막고 있었기에 문제가 발생.
