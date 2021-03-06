import json
import os
import subprocess
import datetime
import re
import time
import math
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
import itertools

with open('/home/ubuntu/data/data.json') as f:
    data = json.load(f)

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}"
os.system(f"mkdir -p {path}")
os.chdir(path)

os.system(f"curl 'https://www.zaitakukanri.co.jp/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3706.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: https://www.zaitakukanri.co.jp/top/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=rtbr8tas9q962vpcl1em2mlsn0' --compressed > zaitakukanri.html")

with open(f"zaitakukanri.html") as f:
    soup = BeautifulSoup(f, 'html5lib')

hash = soup.find('input', {'type':'hidden'}).get('value')
username = soup.find('input', {'type':'text'}).get('id')
password = soup.find('input', {'type':'password'}).get('id')

proc = subprocess.Popen(f"curl -c - 'https://www.zaitakukanri.co.jp/login/index/login/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://www.zaitakukanri.co.jp' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3706.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: https://www.zaitakukanri.co.jp/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=rtbr8tas9q962vpcl1em2mlsn0' --data 'hash={hash}&{username}=3346&{password}=0033' --compressed | grep 'zaitakukanri'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth = '='.join(out.decode('utf-8').strip().split('\t')[5:])

os.system(f"curl 'https://www.zaitakukanri.co.jp/search/?&num=2000' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3605.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=rtbr8tas9q962vpcl1em2mlsn0; {auth}' --compressed > zaitakukanri_top.html")

with open(f"zaitakukanri_top.html") as f:
    soup = BeautifulSoup(f, 'html5lib')

today_new = {}
today_keys = []
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

    room_size = details['間取り']
    table = li.findAll('table')[1]
    details[table.find('th').text.strip()] = table.find('td').text.strip()
    images = {}
    table = li.findAll('table')[2]
    for index, td in enumerate(table.findAll('td')):
        images[f"{td.text}_{index + 1}"] = td.find('img')['data-original'].replace("74_76.jpg", "4000_4000.jpg")

    src_id = list(images.values())[0].split('_')[1]

    if len(details['最寄り駅'].split('/')) < 2:
        continue

    item["line"] = details['最寄り駅'].split('/')[0]
    item["station"] = details['最寄り駅'].split('/')[1]
    item["duration"] = details['駅より']
    item["src_id"] = src_id
    item["date"] = today
    item["site"] = "zaitakukanri"
    item["images"] = images
    item["details"] = details
    item['room_size'] = room_size

    key = f"{item['site']}_{item['src_id']}"
    today_keys.append(key)
    if key in data:
        continue

    size_line_station = f"{room_size}/{item['line']}/{item['station']}"
    # os.system(f"mkdir -p 'zaitakukanri_{src_id}'")
    os.system(f"mkdir -p '/home/ubuntu/data/rooms/{size_line_station}/zaitakukanri_{src_id}/'")
    # os.system(f"mkdir -p '/home/ubuntu/data/images/{size_line_station}/zaitakukanri_{src_id}/'")
    os.system(f"curl 'https://www.zaitakukanri.co.jp/mediate/ajax/downloadzumenexecute/rentId/{src_id}/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3606.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.zaitakukanri.co.jp/search/?&num=2000' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: PHPSESSID=rtbr8tas9q962vpcl1em2mlsn0; {auth}' --compressed > '/home/ubuntu/data/rooms/{size_line_station}/zaitakukanri_{src_id}/doc.jpg'")

    for image_name, image_url in images.items():
        os.system(f"wget -o /dev/null --no-check-certificate -qO '/home/ubuntu/data/rooms/{size_line_station}/zaitakukanri_{src_id}/{image_name}.jpg' 'https://zaitakukanri.co.jp{image_url}'")

    with open(f"/home/ubuntu/data/rooms/{size_line_station}/zaitakukanri_{src_id}/detail.txt", 'w') as f:
        f.write(tabulate(details.items(), tablefmt="simple"))

    # data[key] = item
    today_new[key] = item

with open(f"/home/ubuntu/data/dates/{today}/zaitakukanri.json", "w") as f:
    json.dump(today_new, f, indent=2, sort_keys=False, ensure_ascii=False)

with open(f"/home/ubuntu/data/keys/{today}/zaitakukanri.json", "w") as f:
    json.dump(today_keys, f, indent=2, sort_keys=False, ensure_ascii=False)
