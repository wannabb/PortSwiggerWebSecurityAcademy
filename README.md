# 🛡️ PortSwigger Web Security Academy 풀이 및 정리

PortSwigger Web Security Academy의 모든 주제와 랩(Lab) 풀이 과정을 기록하는 공간입니다.  
**진행 기간:** 2026.06 ~ 진행 중

---

## 📊 진행 상황 (Progress)
```diff
+ Apprentice (초급):   27 / 61
+ Practitioner (중급): 57 / 173
+ Expert (고급):        4 / 39
```
---

## 📚 주제별 학습 및 랩 풀이 (Topics & Labs)

### 1. Server-side vulnerabilities
- [x] **SQL injection**
- [ ] **Authentication** - 진행중...
- [x] **Path traversal**
- [ ] **Command injection**
- [ ] **Business logic vulnerabilities**
- [ ] **Information disclosure**
- [ ] **Access control vulnerabilities**
- [x] **File upload vulnerabilities**
- [x] **Server-side request forgery (SSRF)**
- [ ] **XInclude attacks**

### 2. Client-side vulnerabilities
- [x] **Cross-site scripting (XSS)**
- [x] **Cross-site request forgery (CSRF)**
- [x] **Cross-origin resource sharing (CORS)**
- [ ] **Clickjacking**
- [ ] **DOM-based vulnerabilities**
- [ ] **WebSockets**

### 3. Advanced topics
- [ ] **Insecure deserialization**
- [ ] **GraphQL API vulnerabilities**
- [ ] **Server-side template injection (SSTI)**
- [ ] **Web cache poisoning**
- [ ] **HTTP Host header attacks**
- [ ] **HTTP request smuggling**
- [ ] **OAuth authentication**
- [ ] **JWT attacks**

---

## 📝 랩 풀이 작성 규칙 (Write-up Format)
각 랩 풀이 문서(`lab-xx.md`)는 아래 항목을 포함하여 작성합니다.
1. **문제 요약 (Objective):** 목표 및 주요 취약점
2. **핵심 개념 (Key Concepts):** 관련 개념 및 페이로드 원리
3. **풀이 과정 (Steps):** Burp Suite 요청/응답 분석 및 익스플로잇
4. **대응 방안 (Mitigation):** 취약점의 발생 원인
