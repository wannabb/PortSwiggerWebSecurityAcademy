# 🚩Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

TThis lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality. 
The reflection occurs inside a JavaScript string with single quotes and backslashes escaped.
To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.


### 🔍 분석 및 공격 과정
1. search 기능에서 XSS 취약점이 있다고 함. 임의값을 검색해서 소스코드를 살펴보면 내가 검색한 값은 javascript내에 삽입됨.
```html
<script>
var searchTerms = 'exam';
document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>                    
```
2. 그렇다면 javascript context 상의 XSS라 보고 한번 검색 값으로 `exam'+alert()+'`를 줘봄.
3. `'`에 대해 escape 처리를 하고 있음. 그렇다면 `exam\'+alert()` 를 주어 `'`앞에 붙는 backslash 자체를 escape 시키면?
4. 문제에 적혀있다시피 backslash도 escape처리를 하여 먹히지는 않음.
5. `</script>`를 입력으로 줘봄. -> `<`와 `>`에 대한 처리는 구현되어 있지 않았음. 따라서 </script>로 닫아버리고 새로운 스크립트 태그를 생성하여 solve
```html
</script><script>alert()</script>
```



### 💡 취약점 원리
  `<`, `>`를 막지않는 `javascript context XSS`
