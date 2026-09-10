# Authentication (인증)

## 1. 개요 (Overview)
- **정의:** 사용자의 신원을 보증하는 기술. 사용자가 알고 있는 것(Know), 가지고 있는 것(Have), 고유하게 가진 것(Are) 요소 중 하나 이상을 확인한다.
  - **Know (지식 기반):** Password, PIN 등
  - **Have (소지 기반):** Security Token, Mobile Phone, OTP 등
  - **Are (생체/행동 기반):** 지문, 홍채, 행동 패턴 등

> [!NOTE]
> **Authentication vs Authorization**
> - **Authentication (인증):** 사용자가 *누구인지* 신원을 확인하는 과정
> - **Authorization (인가):** 인증된 사용자가 *어떤 자원에 접근할 수 있는지* 권한을 부여하는 과정

## 2. 공격 메커니즘 (Attack Vector)
인증 메커니즘의 취약점은 크게 두 가지로 나뉜다.

**1) 무차별 대입(Brute Force) 방어 미흡**
- 반복적인 로그인 실패 시 계정 잠금이나 IP 차단을 적용하더라도 다음과 같은 우회점 및 한계가 존재한다.
  - 리버스 프록시 환경에서 `X-Forwarded-For` 헤더를 검증 없이 신뢰하여 IP 차단을 우회함
  - **Password Spraying:** 하나의 흔한 비밀번호로 여러 계정에 1회씩 시도하여 계정 잠금 정책을 회피함
  - **Account Enumeration:** 로그인 실패 시 응답 메시지 차이나 계정 잠금 여부를 통해 실제 존재 유무를 알아냄
  - **Credential Stuffing:** 유출된 계정 목록(ID/PW)을 타 사이트에 재대입하는 공격은 계정 단위 차단이나 단순 IP 차단으로 막기 어려움

**2) 인증 로직의 설계상 결함 (Logical Flaw)**
- Multi-Factor Authentication(MFA)을 도입했더라도 인증 단계별 상태 검증 미흡 등 논리적 결함이 있다면 우회될 수 있다.
- **인증 단계 간 상태 검증 미흡:** 1단계(비밀번호) 인증 후 2단계(OTP)를 거치지 않고 최종 목적지 URL로 직접 접근하거나, 타인의 계정 식별자로 요청을 교체해도 서버가 유효한 인증 상태로 잘못 인지하는 현상
## 3. 대응 방안 (Mitigation)
- 서로 다른 인증 요소(Know, Have, Are)를 결합한 **MFA(다중 요소 인증)**를 구현하되, 각 단계 간 인증 상태 유효성을 검증하여 논리적 결함이 없도록 설계한다.
