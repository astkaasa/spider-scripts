import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

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

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/bukkaku"
os.system(f"mkdir -p {path}")
os.chdir(path)

proc = subprocess.Popen(f"curl -c - 'https://{site}.bukkaku.jp/agent/login/login' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://{site}.bukkaku.jp' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.bukkaku.jp/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'account={username}&password={password}' --compressed | awk '$6 ~ /_session_id/ {{print $7}}'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth = out.decode('utf-8').strip()

os.system(f"curl 'https://{site}.bukkaku.jp/agent/search/list?c%5Bcity_id%5D%5B%5D=13101&c%5Bcity_id%5D%5B%5D=13102&c%5Bcity_id%5D%5B%5D=13103&c%5Bcity_id%5D%5B%5D=13104&c%5Bcity_id%5D%5B%5D=13105&c%5Bcity_id%5D%5B%5D=13106&c%5Bcity_id%5D%5B%5D=13107&c%5Bcity_id%5D%5B%5D=13108&c%5Bcity_id%5D%5B%5D=13109&c%5Bcity_id%5D%5B%5D=13110&c%5Bcity_id%5D%5B%5D=13111&c%5Bcity_id%5D%5B%5D=13112&c%5Bcity_id%5D%5B%5D=13113&c%5Bcity_id%5D%5B%5D=13114&c%5Bcity_id%5D%5B%5D=13115&c%5Bcity_id%5D%5B%5D=13116&c%5Bcity_id%5D%5B%5D=13117&c%5Bcity_id%5D%5B%5D=13118&c%5Bcity_id%5D%5B%5D=13119&c%5Bcity_id%5D%5B%5D=13120&c%5Bcity_id%5D%5B%5D=13121&c%5Bcity_id%5D%5B%5D=13206&c%5Bcity_id%5D%5B%5D=13209&c%5Bcity_id%5D%5B%5D=13210&c%5Broom_search_type%5D%5B%5D=1&c%5Broom_search_type%5D%5B%5D=2&c%5Broom_search_type%5D%5B%5D=3&c%5Broom_search_type%5D%5B%5D=4&c%5Broom_search_type%5D%5B%5D=5&c%5Broom_search_type%5D%5B%5D=10&c%5Broom_search_type%5D%5B%5D=11&c%5Broom_search_type%5D%5B%5D=6&c%5Bmin_rent%5D=&c%5Bmax_rent%5D=&c%5Bshikirei0%5D=0&c%5Binclude_kanrihi%5D=0&c%5Bwalk_minute%5D=&c%5Bage%5D=&c%5Bmin_space%5D=&c%5Bmax_space%5D=&x=15&y=17&c\\[per_page\\]=1000' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed > {site}_all.log")

proc = subprocess.Popen(f"cat {site}_all.log | grep -Eo 'r[0-9]+'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
arr = out.decode('utf-8').split('\n')
arr.pop()
arr = [element.replace('r', '') for element in arr]

proc = subprocess.Popen(f"cat {site}_all.log | grep -A5 'class=\"Access\"'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
arr1 = out.decode('utf-8').split('--')
arr1.pop(0)

line_arr = []
station_arr = []
duration_arr = []

line_arr = [element.strip().split('\n')[2].strip().replace("<br />", "") for element in arr1]
station_arr = [element.strip().split('\n')[3].strip().replace("</span><br />", "").replace("<span>", "") for element in arr1]
duration_arr = [element.strip().split('\n')[5].strip().replace(")", "") for element in arr1]

for index, room_id in enumerate(arr):
	name = f"{line_arr[index]}/{station_arr[index]}/{duration_arr[index]}_{site}_{index}"
	os.system(f"mkdir -p '{name}'")
	os.system(f"curl 'https://{site}.bukkaku.jp/agent/room/spec_pdf/{room_id}?belt_type=manager' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed > '{name}/doc.pdf'")

	proc = subprocess.Popen(f"curl 'https://{site}.bukkaku.jp/agent/room/images/{room_id}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: _session_id={auth}' --compressed | grep -Eo '(http|https)://[a-zA-Z0-9&;./?=_-]*original[a-zA-Z0-9&;./?=_-]*.jpg'", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	images = out.decode('utf-8').split('\n')
	images.pop()
	
	os.chdir(name)
	for image_url in images:
		os.system(f"wget '{image_url}'")

	os.chdir(path)
