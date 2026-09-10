# Authentication (인증)

## 1. 개요 (Overview)

- 정의: 사용자의 신원을 보증하는 기술. 사용자가 가지고 있는 것(Have), 아는 것(Know), (생체정보, 행동의패턴등)(Are) 요소들중 하나 이상을 확인 하기 위해 다양한 기술에 의존한다.
- Know: password, security question... 
- Have: token, mobile phone...
- Are: 생체정보, 행동의 패턴...

> [!NOTE] 
> **Authentication** vs **Authorization** <br>
> Authentication은 **누구인지** 확인하는 과정이고, Authorization은 무엇까지 할 수 있는지 **권한**에 대한 내용.
## 2. 공격 메커니즘 (Attack Vector)
- 인증 메커니즘의 취약점은 대부분 두가지 중 하나이다. <br>
**1) 무차별대입에 대한 방어가 철저하지 않았다.**
  - 무차별대입에 대한 방어로 반복적인 실패시 `계정잠금` 혹은 `IP차단`을 사용하는 경우가 많다.
  - 그러나 만약 리버스 프록시단에서 `X-Forwarded-For` 헤더를 전적으로 신뢰하거나, 로그인을 성공할 경우 시도 횟수 카운터가 초기화 된다던지
  - 아니면 일부러 사전내에 여러가지 아이디를 브루트포스 해보며 잠기게 만들고 실제로 존재하는 ID인지 파악할 수 있는 결함이 있다면 효과적이지 않은 방어이고
  - 또한, `Credential Stuffing`(유출된 계정 목록쌍으로 1번씩 타사이트에 대입해보는 것)은 계정잠금과 IP차단으로 막을 수 없다.
  - 따라서 단일 인증 보다는 Multi Authentication으로 구현해야 한다.<br>
**2) 인증 메커니즘 자체가 논리적으로 효과적이지 않아 우회가 가능한 인증이다.**
  - multi FA라 하더라도 논리적인 결함이 있다면 우회될 수 있다.

## 3. 대응 방안 (Mitigation)
- 서로 다른 인증 요소들(Have, Know, Are)을 결합하여 논리적으로 결함이 없도록 구현하여야 함.
- temp
