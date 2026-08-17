## 1. 출력시 데이터를 인코딩
: 데이터를 페이지에 쓰기 직전에 인코딩을 적용해야 한다. 왜냐하면 데이터를 쓰는 컨텍스트에 따라 필요한 인코딩 유형이 결정되기 때문이다.

html컨텍스트에서는 화이트리스트에 없는 값을 `html엔티티`로 변환해야한다.

JAVAscript 문자열 컨텍스트에서는 영어나 숫자가 아닌 값은 `유니코드 이스케이프` 처리해야 한다.

이벤트 핸들러 내부에 사용자 입력을 포함시킬때는 javascript 컨텍스트와 html 컨텍스트 모두를 처리해야함. 먼저 입력값을 유니코드 이스케이프 처리한 후 HTML인코딩을 해야한다.

## 2. 입력값이 도착하면 유효성을 검사한다.
*:사용자로부터 입력을 처음 받는 시점에서 가능한 엄격하게 입력값을 검증해야한다.*

입력 유효성 검사 예:
- 사용자가 응답으로 반환될 URL을 제출하면 해당 URL이 HTTP 및 HTTPS와 같은 안전한 프로토콜로 시작하는지 검증한다.
- 그렇지 않으면 javascript 나 data 같은 유해한 프로토콜을 악용할 여지가 생긴다.
- 만약 유저가 숫자일 것으로 예측되는 값을 입력시 해당 값이 실제로 정수인지 조차도 검증해야한다.
- 입력값이 예상되는 문자 집합으로만 구성되는지 검증한다. (화이트리스트)

## 3. 안전한 HTML 허용
: 가장 좋은건 사용자가 HTML 마크업을 게시하는 것을 피하는 것이지만, 비즈니스 요구 사항때문에 필요한 경우가 있다. 화이트리스트를 통해 안전한 HTML 태그를 게시하도록 구현할 수 있으나, 브라우저의 파싱엔진의 차이로 인한 XSS 변이 공격에 취약할 수 있다. 즉, 안전해 보인다고 판단한 HTML도 파싱 후에 악성코드 변환될 수 있는 문제에는 취약하다는 것이다. 이때 사용할 수 있는 해결책으로는 `DOMPurify`와 같은 자바스크립트 라이브러리를 활용하여 사용자의 브라우저에서 필터링과 인코딩을 수행하는 것이다. 하지만 이런 라이브러리도 보안적으로 완벽한 해결책은 아니기에 보안 업데이트를 면밀히 모니터링할 필요가 있다.

## 4. 템플릿 엔진을 사용하여 XSS를 방지하기
: 템플릿엔진의 이스케이핑 시스템을 활용하여 동적컨텐츠에 포함되는 민감한 문자는 이스케이핑 처리되도록 면밀히 검토할 것.

## 5. PHP에서 XSS를 방지하기
: PHP에는 다음과 같은 HTML엔티티 인코딩 함수가 있다. `<?php echo htmlentities($input, ENT_QUOTES, 'UTF-8');?>` 
 이 내장함수를 사용해 HTML 컨텍스트 내의 입력을 인코딩하고 이스케이프할 수 있다. 1번에서 서술했다시피 javascript 컨텍스트에서는 유니코드 이스케이프를 해야하는데 PHP에는 유니코드 이스케이프를 처리하는 API가 없다.
 자체적으로 구현해본다면 다음과 같은 함수가 만들어진다.
```php
<?php
function jsEscape($str) {
    $output = '';
    $str = str_split($str);
    for($i=0;$i<count($str);$i++) {
        $chrNum = ord($str[$i]);
        $chr = $str[$i];
        if($chrNum === 226) {
            if(isset($str[$i+1]) && ord($str[$i+1]) === 128) {
                if(isset($str[$i+2]) && ord($str[$i+2]) === 168) {
                    $output .= '\u2028';
                    $i += 2;
                    continue;
                }
                if(isset($str[$i+2]) && ord($str[$i+2]) === 169) {
                    $output .= '\u2029';
                    $i += 2;
                    continue;
                }
            }
        }
        switch($chr) {
            case "'":
            case '"':
            case "\n";
            case "\r";
            case "&";
            case "\\";
            case "<":
            case ">":
                $output .= sprintf("\\u%04x", $chrNum);
            break;
            default:
                $output .= $str[$i];
            break;
    }
    }
    return $output;
}
?>
```
```html
<script>x = '<?php echo jsEscape($_GET['x'])?>';</script>
```

 ## 5. 자바스크립트에서 클라이언트  XSS를 방지하기
 : 자바스크립트 내에서 HTML컨텍스트를 인코딩하는 경우에 안전한 HTML 인코더는 다음과 같다.
```javascript
function HTMLEncode(str){
  return String(str).replace(/[^\w. ]/gi, function(c){
    return '&#' + c.charCodeAt(0) + ';';}
);
}
```
 : 자바스크립트 내에서 javascript컨텍스트를 인코딩하는 경우에 안전한 유니코드 이스케이프는 다음과 같다.
 ```javascript
function jsEscape(str){
  return String(str).replace(w/[^w. ]/gi, function(c){
    return '//u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);});
}
```

## 6. jQuery에서 XSS를 방지하기
 : 구버전의 jQuery에서는 `location.hash`를 사용해 선택자에게 넘겨줄때 때 `#<새로운태그>` 이런 식으로 새로운 태그를 주입할 수 있었으나, 현재는 패치가 이루어져 무조건 첫글자가 `<` 인 경우에만 렌더 하도록 패치됨. 신뢰할 수 없는 데이터를 
 jQuery에 전달할 때는 위의 `jsEscape`같은 함수를 사용해 넘겨줘야 함.

## 7. CSP를 사용하여 XSS 완화하기
: CSP는 XSS 공격에 대한 최후의 방어선으로써 앞의 방어 수단이 우회되었을 경우, 공격자가 할 수 있는 행동을 제한함으로써 그 피해를 줄일 수 있다. [CSP](https://github.com/wannabb/PortSwiggerWebSecurityAcademy/edit/main/XSS/CSP.md)



