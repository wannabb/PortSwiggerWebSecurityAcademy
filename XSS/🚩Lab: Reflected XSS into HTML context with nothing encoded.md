#🚩Lab: Reflected XSS into HTML context with nothing encoded

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
To solve the lab, perform a cross-site scripting attack that calls the alert function.

### 🔍 분석 및 공격 과정
1. Lab에 접속하자 마자 Search를 할 수 있는 박스가 보임.
2. 임의의 키워드로 검색 해보니 `0 search result for '임의의 값` 이렇게 응답에 포함시켜 돌려줌.
3. 이때 search 값으로 `<script> alert(1) </script>`를 주면 응답에 인라인 스크립트로 포함되어 그대로 실행됨. -> solve

### 💡 취약점 원리
 사용자가 입력한 안전하지 않은 값을 검증하거나 인코딩처리 하지 않고 그대로 응답에 포함시켜 돌려주는 reflected XSS의 가장 기본적인 유형이였다.
 입력 값에 대한 `안전한 검증`과 `HTML엔티티 인코딩 처리`가 필요하며, 직접 구현하지 않고 프레임워크에 포함된 XSS 보안 기능을 추가하여 보완해야함.

