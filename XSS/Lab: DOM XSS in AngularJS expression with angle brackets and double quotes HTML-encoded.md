# 🚩Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

This lab contains a DOM-based cross-site scripting vulnerability in a AngularJS expression within the search functionality.
AngularJS is a popular JavaScript library, which scans the contents of HTML nodes containing the `ng-app` attribute (also known as an AngularJS directive). 
When a directive is added to the HTML code, you can execute JavaScript expressions within `double curly braces`. This technique is useful when angle brackets are being encoded.
To solve this lab, perform a cross-site scripting attack that executes an AngularJS expression and calls the `alert` function.


### 🔍 분석 및 공격 과정
1. 해당 문제는 `<>`가 인코딩되지만 AngularJS의 `ng-app`속성을 사용할 때 스크립트를 실행시키는 랩.
2. AngularJS에서는 `ng-app` 속성을 적용시키면 `{{ AngularJS의 표현식 }}`를 이용해 스크립트를 실행할 수 있다.
3. 임의의 문자열인 `exam`을 search 해본다. -> HTML 소스를 살펴보면 body태그에 `ng-app` 속성이 지정되어 있다.
4. `exam`은 h1태그 내부에 반영되어 나타나고 있다. `{{ 1+3 }}`을 search해보면 4로 잘 반영되어 나타난다.
5. AngularJS 표현식 에서는 컨트롤러의 스코프에 정의되지 않은 Javascript의 함수를 호출할 수는 없다. (컨트롤러내부의 $scope에 $scope.함수이름 = function(){...} 이런 식으로 정의되어 있어야 함)
6. 페이로드 작성
7. {{ alert() }} X
8. {{ function('alert()')() }} X
9. 우회해야 함. `constructor` 라는 JS의 기본 프로퍼티를 사용. 만약 빈 문자열에 `''.constructor` 를 주면 `String` 이 되고, String타입.constructor는 `function`이 된다.
10. 그렇다면 `{{ ''.constructor.constructor('alert()')() }}`를 search 한다면 solve
+ 구버전의 AngularJS라 가능한 우회였음.


### 💡 취약점 원리
 고전적인 AngularJS에서 발생할 수 있는 DOM XSS 취약점
