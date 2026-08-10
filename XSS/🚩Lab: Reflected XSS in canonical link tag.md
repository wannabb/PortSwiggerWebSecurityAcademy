# 🚩Lab: Reflected XSS in canonical link tag

This lab reflects user input in a canonical link tag and escapes angle brackets.
To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the alert function.
To assist with your exploit, you can assume that the simulated user will press the following key combinations:

ALT+SHIFT+X
CTRL+ALT+X
Alt+X
Please note that the intended solution to this lab is only possible in Chrome.

### 🔍 분석 및 공격 과정
1. 일단 문제를 먼저 풀기 전에, `accesskey` 속성과 `canonical link tag`에 대해 알아보자.
2. `accesskey`: 단축키와 같은 개념으로써 만약 accesskey='x' 와 같은 속성 값을 준다면 사용자의 환경에 따라 `ALT+X`, `CTRL+ALT+X`, `ALT+SHIFT+X` 와 같은 키를 누르면 해당 요소에 빠르게 접근할 수 있다. (포커싱)
3.  `canonical link tag`: 페이지는 거의 동일하나 URL이 다를 경우 검색엔진에 노출되는 빈도가 분산될 수 있다. 이때 canonical link tag를 이용해 대표 페이지를 명시해준다면 검색에 있어 최적화를 해준다.
   - 다음과 같이 사용된다. <link rel=canonical href="https://대표주소.com/">
4. 이제 본격적으로 문제 페이지를 살펴보자. 루트 페이지에서 소스코드를 살펴본 결과 canonical link tag가 포함되어 있음을 볼 수 있다.
5. 브라우저에 입력된 url을 쿼리 파라미터를 이용해 바꿔보면, href에 입력된 값도 바뀌고 있다.
6. 아마 현재 브라우저에 입력된 URL전체를 href의 값으로 주는 잘못 구현된 canonical link tag인 것 같다.
7. 이런 취약점에 따라 구현된 페이로드는 다음과 같다.
```html
https://0afd00660375e1d283d1aadd00b00008.web-security-academy.net/?%27accesskey=%27x%27onclick=%27alert())
```
8. 다음 url을 브라우저 주면 뒷부분의 쿼리 스트링 자체는 브라우저의 동작자체에 영향을 주지는 않으면서 `<link>` 태그 내에 다음과 같이 삽입된다.
```html
<link rel="canonical" href="https://0afd00660375e1d283d1aadd00b00008.web-security-academy.net/?" accesskey="x" onclick="alert()">
```
9. solve



### 💡 취약점 원리
  canonical 링크 태그 자체의 문제라기 보다는 개발자가 href의 값을 불러오는 구현의 방식이 잘못되었다. 또한, XSS를 막기 위해 `<>`는 HTML 엔티티 인코딩으로 막고 있으나 해당 부분은 `<sciprt>`와 같이
  새로운 태그를 만들어 내는 것을 막을 수 있을 뿐 이였음. `'`와 `"`는 필터링 되지 않아 attribute context XSS가 발생할 수 있었음.
