# 🚩Lab: Stored DOM XSS

This lab demonstrates a stored DOM vulnerability in the blog comment functionality. 
To solve this lab, exploit this vulnerability to call the `alert()` function.

### 🔍 분석 및 공격 과정
1. 개발자 도구의 network탭으로 이동해서 받은 `loadCommentsWithVulnerableEscapeHtml.js` 파일을 살펴본다.
```js
function loadComments(postCommentPath) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let comments = JSON.parse(this.responseText);
            displayComments(comments);
        }
    };
    xhr.open("GET", postCommentPath + window.location.search);
    xhr.send();

    function escapeHTML(html) {
        return html.replace('<', '&lt;').replace('>', '&gt;');
    }

    function displayComments(comments) {
        let userComments = document.getElementById("user-comments");

        for (let i = 0; i < comments.length; ++i)
        {
            comment = comments[i];
            let commentSection = document.createElement("section");
            commentSection.setAttribute("class", "comment");

            let firstPElement = document.createElement("p");

            let avatarImgElement = document.createElement("img");
            avatarImgElement.setAttribute("class", "avatar");
            avatarImgElement.setAttribute("src", comment.avatar ? escapeHTML(comment.avatar) : "/resources/images/avatarDefault.svg");

            if (comment.author) {
                if (comment.website) {
                    let websiteElement = document.createElement("a");
                    websiteElement.setAttribute("id", "author");
                    websiteElement.setAttribute("href", comment.website);
                    firstPElement.appendChild(websiteElement)
                }

                let newInnerHtml = firstPElement.innerHTML + escapeHTML(comment.author)
                firstPElement.innerHTML = newInnerHtml
            }

            if (comment.date) {
                let dateObj = new Date(comment.date)
                let month = '' + (dateObj.getMonth() + 1);
                let day = '' + dateObj.getDate();
                let year = dateObj.getFullYear();

                if (month.length < 2)
                    month = '0' + month;
                if (day.length < 2)
                    day = '0' + day;

                dateStr = [day, month, year].join('-');

                let newInnerHtml = firstPElement.innerHTML + " | " + dateStr
                firstPElement.innerHTML = newInnerHtml
            }

            firstPElement.appendChild(avatarImgElement);

            commentSection.appendChild(firstPElement);

            if (comment.body) {
                let commentBodyPElement = document.createElement("p");
                commentBodyPElement.innerHTML = escapeHTML(comment.body);

                commentSection.appendChild(commentBodyPElement);
            }
            commentSection.appendChild(document.createElement("p"));

            userComments.appendChild(commentSection);
        }
    }
};
``` 
2. 해당 코드를 살펴보니, 동적으로 <p>태그 (comment내용)에만 `escapeHTML`이라는 function을 적용하여 `innerHTML`에 삽입하고 있다.
3. `escapeHTML`함수의 문제점은 replace 함수를 적용하면서도 재귀적이지 않아 `<`와 `>` 태그를 한개씩만 인코딩할 뿐 2개씩 이상 받을 때는 모두 인코딩하지 못 한다는 것이다.
4. 만약 `<><>` 이렇게 입력을 준다면? `&lt;&gt;<>` 이렇게 된다는 점이 문제이다.
5. 페이로드는 다음과 같다. `<><img src=1 onerror=alert()>`


### 💡 취약점 원리
 HTML엔티티 인코딩을 구현하였으나 빈약한 구현.
