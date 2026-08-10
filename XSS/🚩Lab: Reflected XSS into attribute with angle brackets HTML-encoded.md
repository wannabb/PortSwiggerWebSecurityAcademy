# 🚩Lab: Reflected XSS into attribute with angle brackets HTML-encoded

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded. 
To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the alert function.

### 🔍 분석 및 공격 과정
1. `'<' 와 '>'`를 HTML-encoding하고 있음. example이라고 search해본 결과 제출한 값은 <input> 태그내의 값으로 포함됨.
2. " 로 닫아 버리고 새로운 이벤트핸들러를 추가해버리도록 검색값을 수정.
```html
" onclick='alert(1)' x="a
```
3. solve

### 💡 취약점 원리
  `"나 '`는 html인코딩 하지 않았음
