# 🚩Lab: SameSite Strict bypass via client-side redirect

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials:`wiener:peter`

### 🔍 분석 및 공격 과정
1. `wiener:peter` 로 로그인.
2. 로그인시 POST하는 패킷을 프록시로 관찰 -> set-cookie로 설정되는 session쿠키의 `SameSite=strict`. -> crossorigin의 요청에 쿠키를 포함시키지 않음. -> 기존과 다른 방식이 필요함.
3. 즉 애플리케이션에 존재하는 다른 취약점을 찾아내서 애플리케이션 내에서 요청을 만들어 내도록 해야함. 
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
7. 
                        
### 💡 취약점 원리
  
 
