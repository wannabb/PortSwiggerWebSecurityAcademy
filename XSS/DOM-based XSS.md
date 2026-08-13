# [취약점명] DOM-based XSS (cross site scripting)


## 0. 필요 개념
- `DOM`: `HTML`이나 `XML`문서를 파싱하여 각 요소를 계층적으로 구조화한 트리형태의 API.
- 보안 관점의 `source`: `location.search`나 `document.referrer`처럼 `사용자가 제어할 수 있는 데이터`가 들어오는 곳. 
- 보안 관점의 `sink`: 입력된 데이터가 최종적으로 도달하여 실행되거나 렌더링되는 `종착지`로써 적절한 검증이 없을 경우 XSS가 발생할 가능성이 있는 지점.
  
## 1. 개요 (Overview)

- 발생 원인: 사용자가 제어할 수 있는 `source`가 적절한 `sanitization`없는 `sink`에 들어가는 경우 발생할 수 있는 XSS 취약점의 일종이다. 서버를 거치지 않고 클라이언트 사이드에서만 공격 흐름이 발생하는 것이 특징.
 

## 2. 공격 메커니즘 (Attack Vector)
- 웹 애플리케이션 URL을 통해 값을 받아 별다른 검증없이 다음과 같은 싱크로 보낸다고 하자.
```html
<script>
const urlPar = new URLSearchParams(window.location.search); // <- source
const proId = urlPar.get('ProductId');

const outputDiv = document.getElementById('product-viewer');
outputDiv.innerHTML = "선택하신 상품 ID는: " + proId + " 입니다."; // <- sink
</script>
```
- URL의 쿼리스트링을 별 검증 없이 받아 파싱해서 proId에 넣고 최종적으로 innerHTML에 삽입하고 있음.
- 정상적이라면 1, 2, 3 이런 식으로 상품의 id값을 받아가겠지만, 만약 URL을 아래와 같이 수정한다면 XSS가 발생함.
```https://취약한 페이지.com/?ProductId=<img src=1 onerror='악성페이로드'>```

## 3. DOM-based XSS 로 인해 생길 수 있는 피해 (Impact of  DOM-based XSS)
- 피해자 유저를 가장하여 피해자 유저가 할 수 있는 모든 기능과 데이터 검색, 수정을 할 수 있음.
- 또한 피해자 유저를 가장해 또 다른 유저에게 공격을 수행 가능. 


## tip. DOM invader
