### 개념
 - Blind SQL injection은 쿼리를 통한 답이 HTTP 응답에 포함되지 않을 경우 사용될 수 있는 공격 기법이다.
 - 실제로 적용하는 방법은 다양하다.

### Exploiting blind SQL injection by triggering conditional responses (Boolean-based blind SQL injection)

 조건이 참이 될때의 반응과 조건이 참이 아닐때의 반응 차이를 통해 이용할 수 있다.
예를 들어 애플리케이션이 쿠기의 sid라는 값을 받으며 그 값이 xyz라고 해보자.
그렇다면 애플리케이션이 DB에 적용할 쿼리는 SELECT * FROM DB1 where sid = 'xyz' 이다.
여기서 sid는 SQL injection을 적용할 수 있는 entry point가 된다. 만약 sid가 xyz인 데이터가 DB1에 실제로 있다면
응답이 "Grant!" 이런 식으로 알람을 보내는 것이고, 실패시 응답은 "Unvalid sid!" 라고 해보자.

 그렇다면 sid를 xyz' AND '1'='1, xyz' AND '1'='2 이렇게 각각 참인 조건, 거짓인 조건을 줄 때 반응이 차이가 난다는 것을 볼 수 있을 것이다.
이 점을 이용하여 DB에 있는 정보(예를 들어 계정의 비밀번호라던지)를 추론해낼 수도 있다. 

 일단 상황은 Users테이블 내에 Admin이라는 Username이 있고 그 계정의 Password를 알아내고 싶은데 SQL injection 쿼리의 결과를 HTTP 응답에 포함시키지 않으며 entry point는 sid라는 쿠키라고
해보자. 이 상황에 적용 해보면 쿼리문은 다음과 같이 보낼 수 있다. 
>>> sid = xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Admin'), 1, 1) > 'm
 이 쿼리를 해석해보자면, `Admin`의 `Password`를 가져와 1부터 1까지 슬라이싱한것이 'm' 보다 큰가? 크다면 true 아니면 false.
왜 하필 m인지를 생각해보면 이분 탐색을 떠올려보면 쉽게 이해할 수 있다. 그렇다면 결과에 따라 다음 알파벳은 무엇으로 정해야할지 쉽게 기준이 설것이다.

### Exploiting blind SQL injection by triggering conditional errors (Error-based blind SQL injection)

 Boolean-based에서는 조건이 참 혹은 거짓일 때 웹사이트에 나타나는 차이가 있어야만 가능했다. 만약 두 경우 모두 웹사이트가 동일한 반응을 낼 경우,
아무것도 할 수 없다. 이때 써볼 수 있는게 바로 Error-based blind SQL injection 이다. 예문을 보면 바로 이해할 수 있다.
>>> xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
>>> xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
 예문을 보면 CASE라는 키워드를 사용하고 있고 WHEN절이 참이면 `1/0` 을 실행하고 아니라면 'a'를 반환하여 'a'와 같은지 확인할 것이다.
근데 `1/0`는 `zero divide`이기에 에러를 출력한다. 이게 바로 Erro-based 이다. 
이정도만 확인하면 사실 사용방법은 Boolean-based와 비슷할 것임을 알 수 있다.
>>> xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
 이런 식으로 말이다.
