# 🚩Lab: SameSite Lax bypass via method override

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter

Note
The default SameSite restrictions differ between browsers. As the victim uses Chrome, we recommend also using Chrome (or Burp's built-in Chromium browser) to test your exploit.

### 🔍 분석 및 공격 과정
1. `wiener:peter` 로 로그인.
2. 로그인시 POST하는 패킷을 프록시로 관찰 -> set-cookie로 설정되는 session쿠키에 별도 SameSite 설정 없음. -> 크롬환경이기에 기본 값인 Lax로 설정됨 -> 크로스 오리진에서는 Get요청이거나 메인 프레임의 이동일시에만 쿠키를 포함 시킴.
3. 이번에는 이메일을 변경하는 요청을 프록시로 관찰해봄. -> POST할 때 session 쿠키와 email값을 포함시키고 있음.
4. 공격자는 피해자가 악성 웹사이트에 접속하도록 유도하여 타겟 서버로 이메일 변경 요청을 보내도록 해야 한다. 하지만 Cross-Origin 환경에서 POST 요청을 보내면 SameSite=Lax 정책으로 인해 session 쿠키가 전송되지 않는다.
5 `<form>` 태그의 기본 method 속성은 GET으로 지정하여 브라우저가 `Top-level navigation` 시 `SameSite=Lax` 쿠키를 포함하여 요청을 보내게 만든다. 이때 백엔드 프레임워크(Symfony)의 Method Override 기능을 이용하기 위해 `<input name="_method" value="POST">` 폼데이터로 함께 전달하면, 서버는 이 GET 요청을 내부적으로 POST 요청으로 재파싱하여 처리힘
```html
<form action="targetserver/change-email">
    <input name="_method" value="POST">
    <input name="email" value ="hack@d">
</form>
<script>
    document.forms[0].submit();
</script>
```
                        
### 💡 취약점 원리
  1. **SameSite=Lax 정책의 우회 조건:**
   - Chrome 등 현대 브라우저의 기본값인 `SameSite=Lax`는 Cross-Site `POST` 요청 시 세션 쿠키 전송을 차단하지만, `GET` 요청을 통한 Top-level Navigation(페이지 이동) 시에는 쿠키를 함께 전송합니다.

2. **HTTP Method Override 기능의 오용:**
   - HTML Form은 기본적으로 GET/POST만 지원하므로, 프레임워크(Symfony)는 `_method` 파라미터나 헤더를 통해 HTTP 메서드를 스위칭하는 **Method Override** 기능을 제공합니다.
   - 서버의 백엔드가 GET 요청으로 전달된 `_method=POST` 파라미터까지 수용하여 메서드를 오버라이드하도록 허용할 경우, 보안 경계의 불일치가 발생합니다.

3. **결과:**
   - 브라우저 레이어: `GET` 요청으로 인식하여 `SameSite=Lax` 세션 쿠키를 정상 부착함.
   - 서버 레이어: `_method=POST` 파라미터에 의해 `POST` 요청으로 인식하여 이메일 변경 로직 수행.
   - 결과적으로 CSRF 방어가 완전히 무력화됨.
