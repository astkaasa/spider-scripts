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

# kankyo-station;73692n;tw1a
# dainichi;51447v;vg77
# joint-property;514416;8whc
# cic;51445n;nj0k
# tosei-com;74953r;te12
# rio;51438i;t8cr
# mdi;51446i;4aya
# grandvan;658466;v16t
# dualtap;104640d;jfam
site, username, password = sys.argv[1].split(';')

with open('/home/ubuntu/data/data.json') as f:
    data = json.load(f)

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}"
os.system(f"mkdir -p {path}")
os.chdir(path)

proc = subprocess.Popen(f"curl -c - 'https://{site}.bukkaku.jp/agent/login/login' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://{site}.bukkaku.jp' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.bukkaku.jp/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'account={username}&password={password}' --compressed | awk '$6 ~ /_session_id/ {{print $7}}'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth = out.decode('utf-8').strip()

os.system(f"curl 'https://{site}.bukkaku.jp/agent/search/list?&c\\[per_page\\]=1000' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3603.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://kankyo-station.bukkaku.jp/agent/search/by_area' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed > {site}_all.log")

with open(f"{site}_all.log") as f:
    soup = BeautifulSoup(f, 'html5lib')

today_new = {}
today_keys = []
table = soup.find("table", { "id" : "roomList" })
arr = table.findAll("tr")
headers = []
th = arr.pop(0).findAll("th")
headers.append(th[1].text.strip())
headers.append(th[2].text.strip())
headers.append(th[3].text.strip())
headers.append(th[4].text.strip())
headers.append(th[5].text.strip())
headers.append(th[6].text.strip())
headers.extend(re.split(r'[\n\t ]+', th[7].text.strip()))
headers.append(th[8].text.strip())
arr1 = re.split(r'[\n\t ]+', th[9].text.strip())
headers.append(arr1[0])
headers.append(arr1[1])
for tr in arr:
    try:
        item = {}
        details = {}
        contents = []
        room_id = tr.get('id').replace('r', '')
        td = tr.findAll("td")
        if td[0].find('span'):
            continue

        room_size = re.search('[1-9][LDSKR]+|$', ' '.join(re.split(r'[\n\t ]+', td[1].text.strip()))).group()
        if not bool(room_size):
            room_size = '-'

        contents.append(' '.join(re.split(r'[\n\t ]+', td[1].text.strip())))
        contents.append(td[3].text.strip())
        contents.append('/'.join(re.split(r'[\n\t ]+', td[4].text.strip())))
        contents.append(td[5].text.strip())
        access_arr = re.split(r'[\n\t ]+', td[6].text.strip())
        line = access_arr[0]
        station = access_arr[1]
        duration = access_arr[2] + access_arr[3]
        contents.append(' '.join(re.split(r'[\n\t ]+', td[6].text.strip())))
        contents.append(' '.join(re.split(r'[\n\t ]+', td[7].text.strip())))
        arr1 = re.split(r'[\n\t ]+', td[8].text.strip())
        contents.append(' '.join(arr1[0:-2]))
        contents.append(arr1[-2])
        contents.append(arr1[-1])
        contents.append(td[9].text.strip())
        contents.extend(re.split(r'[\n\t ]+', td[10].text.strip()))
        for index, header in enumerate(headers):
            details[header] = contents[index]

        item["line"] = line
        item["station"] = station
        item["duration"] = duration
        item["src_id"] = room_id
        item["date"] = today
        item["site"] = f"bukkaku_{site}"
        item["details"] = details
        item["images"] = {}
        item['room_size'] = room_size

#
#
# td = arr[1].findAll("td")
# for item in td:
#     print(re.split(r'[\n\t ]+', item.text.strip()))
#
#
# proc = subprocess.Popen(f"cat {site}_all.log | grep -Eo 'r[0-9]+'", stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()
# arr = out.decode('utf-8').split('\n')
# arr.pop()
# arr = [element.replace('r', '') for element in arr]
#
# proc = subprocess.Popen(f"cat {site}_all.log | grep -A5 'class=\"Access\"'", stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()
# arr1 = out.decode('utf-8').split('--')
# arr1.pop(0)
#
# line_arr = []
# station_arr = []
# duration_arr = []
#
# line_arr = [element.strip().split('\n')[2].strip().replace("<br />", "") for element in arr1]
# station_arr = [element.strip().split('\n')[3].strip().replace("</span><br />", "").replace("<span>", "") for element in arr1]
# duration_arr = [element.strip().split('\n')[5].strip().replace(")", "") for element in arr1]
#

# for index, room_id in enumerate(arr):
#     try:
#         item = {}
#         item["line"] = line_arr[index]
#         item["station"] = station_arr[index]
#         item["duration"] = duration_arr[index]
#         item["src_id"] = room_id
#         item["date"] = today
#         item["site"] = f"bukkaku_{site}"
#         item["images"] = {}

        key = f"{item['site']}_{item['src_id']}"
        today_keys.append(key)
        if key in data:
            continue

        name = f"bukkaku_{site}_{room_id}"
        size_line_station = f"{room_size}/{item['line']}/{item['station']}"
        # os.system(f"mkdir -p '{name}'")
        os.system(f"mkdir -p '/home/ubuntu/data/rooms/{size_line_station}/{name}/'")
        # os.system(f"mkdir -p '/home/ubuntu/data/images/{size_line_station}/{name}/'")
        os.system(f"curl 'https://{site}.bukkaku.jp/agent/room/spec_pdf/{room_id}?belt_type=manager' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed > '/home/ubuntu/data/rooms/{size_line_station}/{name}/doc.pdf'")
        os.system(f"convert -density 300 '/home/ubuntu/data/rooms/{size_line_station}/{name}/doc.pdf' '/home/ubuntu/data/rooms/{size_line_station}/{name}/doc.jpg'")
        os.system(f"rm '/home/ubuntu/data/rooms/{size_line_station}/{name}/doc.pdf'")

        proc = subprocess.Popen(f"curl 'https://{site}.bukkaku.jp/agent/room/images/{room_id}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed | grep 'image_files'", stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        images = []
        images = out.decode('utf-8').split('\n')
        images.pop()

        # os.chdir(name)
        for image_index, image in enumerate(images):
            image_url = re.search(r'(http|https)://[a-zA-Z0-9&;./?=_-]*original[a-zA-Z0-9&;./?=_-]*', image).group(0)
            image_name = image.split('img alt="')[1].split('" src')[0]
            item["images"][f"{image_name}_{image_index}"] = image_url
            os.system(f"wget -o /dev/null -qO '/home/ubuntu/data/rooms/{size_line_station}/{name}/{image_name}_{image_index}.jpg' '{image_url}'")


        with open(f"/home/ubuntu/data/rooms/{size_line_station}/{name}/detail.txt", 'w') as f:
            f.write(tabulate(details.items(), tablefmt="simple"))

        # data[key] = item
        today_new[key] = item
        # os.chdir(path)
    except Exception as e:
        continue

with open(f"/home/ubuntu/data/dates/{today}/bukkaku_{site}.json", "w") as f:
    json.dump(today_new, f, indent=2, sort_keys=False, ensure_ascii=False)

with open(f"/home/ubuntu/data/keys/{today}/bukkaku_{site}.json", "w") as f:
    json.dump(today_keys, f, indent=2, sort_keys=False, ensure_ascii=False)
