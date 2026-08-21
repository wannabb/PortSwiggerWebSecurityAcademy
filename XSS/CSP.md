# CSP - Contents Security Policy

## 1. 개요 (Overview)

- 개념: CSP의 주요 목표는 XSS 공격을 완화하고 보고하는 것입니다. XSS 공격은 서버에서 받은 콘텐츠를 브라우저가 신뢰한다는 점을 악용합니다.
  브라우저는 콘텐츠의 출처를 신뢰하기 때문에 악성 스크립트가 어디서 유입되었든 서버로 부터 받은 것이라면 악성 스크립트를 피해자의 브라우저에서 실행합니다.
  CSP를 사용하면 서버 관리자가 브라우저에서 실행 가능한 스크립트의 유효한 소스로 간주해야 하는 도메인을 지정하여 XSS가 발생할 수 있는 벡터를 줄이거나 제거할 수 있습니다.
  그러면 CSP 호환 브라우저는 허용된 도메인에서 받은 소스 파일에서 로드된 스크립트만 실행하고 HTML 속성을 포함한 인라인 스크립트 및 이벤트 처리 등의 다른 모든 스크립트는 무시합니다.
  궁극적인 보호 형태로서 스크립트 실행을 허용하지 않으려는 사이트는 전역적으로 스크립트 실행을 허용하지 않도록 선택할 수 있습니다.

## 2. 작동
- HTTP 응답의 `Content-Security-Policy` 헤더에 설정된 정책을 포함시켜 보냅니다. 
- 브라우저는 헤더의 값을 바탕으로 페이지 내에서 로드되거나 실행되는 자원(스크립트, 이미지, 스타일 등)의 출처를 검사하고, 허용된 정책과 일치하지 않는 자원의 로드나 실행을 차단합니다.

## 3. 주요 디렉티브와 설정 예시

- `default-src`: 스크립트 나 이미지 등 개별 리소스별 규칙이 따로 없을 경우, 공통으로 적용될 기본 허용 출처를 지정.
- `script-src`: 실행 가능한 JavaScript 스크립트의 허용 출처를 지정.
- `style-src`: CSS 스타일시트의 허용 출처를 지정.
- `img-src`: 이미지 파일의 허용 출처를 지정.
- `frame-ancestors`: 현재 페이지를 <iframe>, <frame> 등으로 로드할 수 있는 출처를 지정.
- `nonce-난수`: 서버는 페이지를 응답할 때마다 임의의 난수를 생성해 그 값을 스크립트 태그들에 삽입한다. 매번 새로운 난수를 생성해내기에 공격자가 만들어낸 태그는 무력화된다.
-  `sha(256, 384, 512등)-스크립트의 해시값`: 신뢰할 수 있는 스크립트의 해시값을 사전에 등록해놓는 방식이다.
```html
설정 예시 -> Content-Security-PolicyL default-src 'self'; script-src 'self' https://신뢰할 수 있는 사이트;
```

## 4. 주의 사항

- 외부 스크립트의 허용 출처로 `CDN`을 줄 경우, 고객별 URL을 사용하지 않는 CDN이라면 제 3자로부터 업로드된 악성 스크립트 또한 허용 되기에 주의해야 한다.
- CSP가 <script>태그를 막는 것은 일반적이지만 많은 CSP가 이미지 요청을 하는 것은 허용하고 있다.즉, 이미지 태그를 이용해 외부서버로 CSRF토큰 같은 민감한 정보를 유출하는 것이 가능하다. 따라서 `img-src` 설정에 유의할 것.
- 일부 정책은 매우 엄격하여 외부요청을 모든 형태의 외부요청을 막지만, 사용자 상호작용을 유도하여 이러한 제한을 우회하는 방법도 존재한다. [엄격한CSP우회](https://github.com/wannabb/PortSwiggerWebSecurityAcademy/blob/main/XSS/%F0%9F%8F%B4Lab%3A%20Reflected%20XSS%20protected%20by%20very%20strict%20CSP%2C%20with%20dangling%20markup%20attack.md)

- 엣지브라우저에서는 유효하지 않은 CSP정책을 받을 때 전채 CSP를 무시하는 특징 존재
- 가끔 `report-uri` directive 를 이용해 사용자가 입력한 값이 정책에 반영되는 웹사이트도 존재한다.
- 크롬의 경우 `script-src-elem` directive가 존재하는데 이건 뒤에 입력되어도 앞에 입력된 `script-src`의 <script> 태그 제어를 덮을 수 있다. `script-src "unsafe-inline"`이라면 인라인 스크립트를 허용하도록 정책을 덮어쓸 수 있다. [활용 심화 랩](https://github.com/wannabb/PortSwiggerWebSecurityAcademy/blob/main/XSS/%F0%9F%8F%B4Lab%3A%20Reflected%20XSS%20protected%20by%20CSP%2C%20with%20CSP%20bypass.md)
