# 🚩Lab: Reflected DOM XSS

This lab demonstrates a reflected DOM vulnerability. 
Reflected DOM vulnerabilities occur when the server-side application processes data from a request and echoes the data in the response. 
A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.
To solve this lab, create an injection that calls the `alert()` function.



### 🔍 분석 및 공격 과정
1. 임의의 문자열 `exam`을 search. 개발자 도구의 네트워크 탭을 이용해 오가는 패킷들을 확인. `search-results?search=exam`를 확인해보니 `{"results":[],"searchTerm":"exam"}` JSON 형태로 내가 검색한 값을 받고 있음.
2. 그리고 `searchResults.js`로 전달되어 동적으로 검색 결과를 렌더링함. 해당 JS파일을 살펴보니 eval 함수를 쓰고 있음.
```html
function search(path) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            eval('var searchResultsObj = ' + this.responseText); //eval 사용중..
            displaySearchResults(searchResultsObj);
        }
    };
    xhr.open("GET", path + window.location.search);
    xhr.send();

    function displaySearchResults(searchResultsObj) {
        var blogHeader = document.getElementsByClassName("blog-header")[0];
        var blogList = document.getElementsByClassName("blog-list")[0];
        var searchTerm = searchResultsObj.searchTerm //JSON의 searchTerm
        var searchResults = searchResultsObj.results //JSON의 result

        var h1 = document.createElement("h1");
        h1.innerText = searchResults.length + " search results for '" + searchTerm + "'";
        blogHeader.appendChild(h1);
        var hr = document.createElement("hr");
        blogHeader.appendChild(hr)

        for (var i = 0; i < searchResults.length; ++i)
        {
            var searchResult = searchResults[i];
            if (searchResult.id) {
                var blogLink = document.createElement("a");
                blogLink.setAttribute("href", "/post?postId=" + searchResult.id);

                if (searchResult.headerImage) {
                    var headerImage = document.createElement("img");
                    headerImage.setAttribute("src", "/image/" + searchResult.headerImage);
                    blogLink.appendChild(headerImage);
                }

                blogList.appendChild(blogLink);
            }

            blogList.innerHTML += "<br/>";

            if (searchResult.title) {
                var title = document.createElement("h2");
                title.innerText = searchResult.title;
                blogList.appendChild(title);
            }

            if (searchResult.summary) {
                var summary = document.createElement("p");
                summary.innerText = searchResult.summary;
                blogList.appendChild(summary);
            }

            if (searchResult.id) {
                var viewPostButton = document.createElement("a");
                viewPostButton.setAttribute("class", "button is-small");
                viewPostButton.setAttribute("href", "/post?postId=" + searchResult.id);
                viewPostButton.innerText = "View post";
            }
        }

        var linkback = document.createElement("div");
        linkback.setAttribute("class", "is-linkback");
        var backToBlog = document.createElement("a");
        backToBlog.setAttribute("href", "/");
        backToBlog.innerText = "Back to Blog";
        linkback.appendChild(backToBlog);
        blogList.appendChild(linkback);
    }
}
```
3. eval은 포함된 함수도 작동시켜버리기에 그냥 JSON에 반환되는 searchTerm이 ""-alert() 가 되도록 하면 됨.
4. 기존의 응답 JSON의 형태가 `{"results":[],"searchTerm":"exam"}` 이기에, `"`로 닫아 버리고 `+alert()`를 붙이고 `}` 로 JSON 데이터 닫고, `//`로 뒤는 주석처리 해버리면 끝.
5. 페이로드 = "+alert()}// -> 작동안함. 보니까 "는 `\`를 붙여 이스케이프 처리를 하고 있음.
6. 혹시나 `\`도 이스케이프 처리하는지 한번 보내봄. -> `\` 자체는 이스케이프 처리하고 있지 않음. 그렇다면 기존의 페이로드에서 "를 \" 로 수정해준다면 이스케이프 처리후 \\"가 되어 우회가능함.
7. 최종 페이로드 = `\"+alert()}//` solve 


### 💡 취약점 원리
 사용자가 입력한 값이 서버로 보내지고 그로부터 받은 응답으로 JS를 실행해 페이지에 렌더링하는 case였다. (Reflected XSS와 DOM XSS의 혼합) . 문제는 안전하지 않은 입력값 처리와 eval함수의 사용이 문제였다.
