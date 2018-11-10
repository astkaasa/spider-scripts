import json
import os
import subprocess
import datetime
import re
import time
import math
import sys
from bs4 import BeautifulSoup
import itertools

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/zaitakukanri"
os.system(f"mkdir -p {path}")
os.chdir(path)

os.system(f"curl 'https://www.zaitakukanri.co.jp/search/?&num=2000' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3605.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=mmv5s2mqcvl9hma6je3vj7hmp5; _4fb564bf9277a72b766d6f3255e0f4b0=b5192df9438f397238a4b11a23e6be38' --compressed > zaitakukanri.html")

with open(f"temp") as f:
    soup = BeautifulSoup(f, 'html5lib')

data = []
for li in soup.findAll('li', {'class':'list-section'}):
    item = {}
    table = li.findAll('table')[0]
    for br in table.find_all("br"):
        br.replace_with("\n" + br.text)

    details = {}
    headers = list(itertools.chain.from_iterable([e.text.split('\n') for e in table.findAll('th')]))
    tds = list(itertools.chain.from_iterable([e.text.split('\n') for e in table.findAll('td')]))
    headers.insert(7, '築年月')
    for index, header in enumerate(headers):
        details[header] = tds[index]

    table = li.findAll('table')[1]
    details[table.find('th').text.strip()] = table.find('td').text.strip()
    images = {}
    table = li.findAll('table')[2]
    for index, td in enumerate(table.findAll('td')):
        images[f"{td.text}_{index + 1}"] = td.find('img')['data-original'].replace("74_76.jpg", "4000_4000.jpg")

    src_id = list(images.values())[0].split('_')[1]
    os.system(f"mkdir -p 'zaitakukanri_{src_id}'")
    os.system(f"curl 'https://www.zaitakukanri.co.jp/mediate/ajax/downloadzumenexecute/rentId/{src_id}/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3606.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.zaitakukanri.co.jp/search/?&num=2000' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=mmv5s2mqcvl9hma6je3vj7hmp5; _4fb564bf9277a72b766d6f3255e0f4b0=b5192df9438f397238a4b11a23e6be38' --compressed > zaitakukanri_{src_id}/doc.jpg")

    item["line"] = details['最寄り駅'].split('/')[0]
    item["station"] = details['最寄り駅'].split('/')[1]
    item["duration"] = details['駅より']
    item["src_id"] = src_id
    item["date"] = today
    item["site"] = "zaitakukanri"
    item["images"] = images
    data.append(item)

    for image_name, image_url in images.items():
        os.system(f"wget --no-check-certificate -qO 'zaitakukanri_{src_id}/{image_name}.jpg' 'https://zaitakukanri.co.jp{image_url}'")

with open(f"/home/ubuntu/{today}/zaitakukanri/data.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)
