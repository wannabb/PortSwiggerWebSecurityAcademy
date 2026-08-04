# 🚩Lab: Stored XSS into HTML context with nothing encoded


This lab contains a stored cross-site scripting vulnerability in the comment functionality.
To solve this lab, submit a comment that calls the alert function when the blog post is viewed.


### 🔍 분석 및 공격 과정
1. `comment`기능에서 검증을 하지 않아 `stored XSS` 취약점 발생하고 있다.
2. `comment`에서 다음의 댓글을 작성하면 해당 스크립트는 DB에 저장되어 자료를 요청받은 브라우저에게 전달된 후 실행된다.

```html
<script>
alert(1);
</script>
```

3. solve


### 💡 취약점 원리
 stored XSS 취약점을 이용해, 악성스크립트를 주입하였다.
