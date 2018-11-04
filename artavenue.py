import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

# http://www.artavenue.co.jp/artproperty/
# ＩＤ：  artp
# PASSWORD:   5010
# site, username, password = sys.argv[1].split(';')

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/artavenue"
os.system(f"mkdir -p {path}")
os.chdir(path)

os.system(f"curl 'https://www.artavenue.co.jp/artproperty/search.php?dv=1000' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Authorization: Basic YXJ0cDo1MDEw' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3544.2 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=5nqm180r68uqi21p8bak9hsuc1' --compressed > all.log")

uid_arr = []
proc = subprocess.Popen("cat all.log | grep -Eo 'detail\\.php\\?uid=[0-9]+' | uniq | grep -Eo '[0-9]+'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
uid_arr = out.decode('utf-8').strip().split('\n')

line_station_arr = []
duration_arr = []
proc = subprocess.Popen("cat all.log | grep -A1 '沿線1'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
line_station_arr = [element.strip().split('\n')[1].strip().replace('<td>', '').replace('</td>', '').split(' ')[0] for element in out.decode('utf-8').split('--')]
duration_arr = [element.strip().split('\n')[1].strip().replace('<td>', '').replace('</td>', '').split(' ')[-1] for element in out.decode('utf-8').split('--')]

for index, uid in enumerate(uid_arr):
  name = f"{line_station_arr[index]}/{duration_arr[index]}_artavenue_{uid}"
  os.system(f"mkdir -p '{name}'")
  os.system(f"curl 'https://www.artavenue.co.jp/artproperty/get_pct.php?uid={uid}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Authorization: Basic YXJ0cDo1MDEw' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3544.2 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.artavenue.co.jp/artproperty/search.php?dv=300' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=5nqm180r68uqi21p8bak9hsuc1' --compressed > '{name}/{uid}.zip'")
  os.system(f"unzip '{name}/{uid}.zip' -d '{name}'")
  os.system(f"rm '{name}/{uid}.zip'")
  os.system(f"wget -O '{name}/doc.pdf' 'http://133.162.209.3:8080/search/SearchResultDetails.do?unit_id={uid}&printmode=3'")
