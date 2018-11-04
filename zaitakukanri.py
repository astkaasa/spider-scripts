import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/zaitakukanri"
os.system(f"mkdir -p {path}")
os.chdir(path)

auth=$(curl -c - 'http://www.zaitakukanri.co.jp/index.php/auth/login' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: http://www.zaitakukanri.co.jp' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://www.zaitakukanri.co.jp/index.php/auth/login' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,ja;q=0.6' --data 'username=3346&password=0033&x=169&y=25' --compressed | awk '$0 ~ /chuukai_ci_session/ {print $7}')

f"curl 'http://www.zaitakukanri.co.jp/index.php/result/all' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,ja;q=0.6' -H "Cookie: pron_ip=8; chuukai_ci_session=${auth}" --data 'search=&limit=1000&order=sort+ASC&page=1&type_id=1&search_target=all' --compressed > doc1"

var1="d957306a3fe529fa271ce1d56797bdde84e70343"
curl 'http://www.zaitakukanri.co.jp/index.php/result/detail/d957306a3fe529fa271ce1d56797bdde84e70343' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,ja;q=0.6' -H "Cookie: pron_ip=8; chuukai_ci_session=${auth}" --compressed

wget "http://www.zaitakukanri.co.jp/files/${var1}_9999.pdf"
wget "http://www.zaitakukanri.co.jp/files/${var1}_00.jpg"
wget "http://www.zaitakukanri.co.jp/files/${var1}_01.jpg"
