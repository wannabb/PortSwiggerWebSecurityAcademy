# [취약점명] XSS - Stored XSS (cross site scripting)

## 1. 개요 (Overview)

- 발생 원인: 애플리케이션이 사용자로 받은 값을 검증하지 않고 그대로 저장하여 이후에 안전하지 않은 방식으로 응답에 포함시켜 돌려줄 경우 발생하는 XSS의 일종이다.

## 2. 공격 메커니즘 (Attack Vector)
- 애플리케이션에 블로그 포스트에 `comment`를 작성하는 기능이 있다고 하자. 예를 들어 `comment`를 작성할 때 다음과 같은 `HTTP 요청`을 보낸다고 가정하자.
```html
POST /post/comment HTTP/1.1
Host: vulnerable-website.com
Content-Length: 100

postId=3&comment=This+post+was+extremely+helpful.&name=Carlos+Montoya&email=carlos%40normal-user.net
```
- 해당 `comment`는 애플리케이션의 데이터베이스에 저장되어 이후 해당 블로그 포스트를 불러오는 요청에 포함시켜 돌려준다. 다음과 같이 말이다.
```html
<p>This post was extremely helpful.</p>
```
- 이때 애플리케이션이 제출된 데이터에 대해 어떠한 처리도 거치지 않는다고 가정하자. 
- 만약, 유저가 제출한 `comment`가  `<script> mailcious code </script>` 라면?
- 해당 포스트를 요청한 유저들은 악성코드가 포함된 응답을 받게되어 그들의 세션을 가지고 브라우저에서 실행되게 된다.
  
## 3. Stored XSS로 인해 생길 수 있는 피해 (Impact of Stored XSS)
- 피해자 유저를 가장하여 피해자 유저가 할 수 있는 모든 기능과 데이터 검색, 수정을 할 수 있음.
- 또한 피해자 유저를 가장해 또 다른 유저에게 공격을 수행 가능. 


  
