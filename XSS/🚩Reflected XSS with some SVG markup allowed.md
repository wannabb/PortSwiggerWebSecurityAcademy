# 🚩Lab: Reflected XSS with some SVG markup allowed

This lab has a simple reflected XSS vulnerability. 
The site is blocking common tags but misses some SVG tags and events.
To solve the lab, perform a cross-site scripting attack that calls the alert() function.

### 🔍 분석 및 공격 과정
1. search기능에서 `<svg>` 태그는 허용되고 있는 랩
2. 그외에 어떤 태그가 또 허용되는지 퍼징해본 결과 `<image>`, `<animatetransform>`태그 사용 가능하고, 이벤트핸들러는 `onbegin` 사용가능. animatetransform은 animate의 대상이 변환(회전, 이동, 스케일링등)에 한정된 animate 태그라고 보면됨.
```html
<svg><image src=javascript:alert(1)></image></svg>
```
3. `javascript:` 스킴은 막혀있는거 같음. `<animatetransform>`태그와 `onbegin`핸들러를 결합해서 사용해보자.
```html
<svg><animatetransform onbegin=alert(1) /></svg>
```
4. solve




### 💡 취약점 원리
  svg태그를 이용한 XSS
