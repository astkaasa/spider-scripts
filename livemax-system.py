import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

# chukai;livemax1500;livemax1500
# site, username, password = sys.argv[1].split(';')

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/livemax-system"
os.system(f"mkdir -p {path}")
os.chdir(path)

page = 1
os.system(f"curl 'https://chukai.setup-chintai.com/search/list.html' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Authorization: Basic bGl2ZW1heDE1MDA6bGl2ZW1heDE1MDA=' -H 'Origin: https://chukai.setup-chintai.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://chukai.setup-chintai.com/search/list.html' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'mode=shousai&page={page}&rosen_id%5B%5D=1&rosen_id%5B%5D=2&rosen_id%5B%5D=3&rosen_id%5B%5D=4&rosen_id%5B%5D=5&rosen_id%5B%5D=6&rosen_id%5B%5D=10&rosen_id%5B%5D=11&rosen_id%5B%5D=13&rosen_id%5B%5D=19&rosen_id%5B%5D=31&rosen_id%5B%5D=32&rosen_id%5B%5D=33&rosen_id%5B%5D=34&rosen_id%5B%5D=38&rosen_id%5B%5D=40&rosen_id%5B%5D=41&rosen_id%5B%5D=42&rosen_id%5B%5D=43&rosen_id%5B%5D=44&rosen_id%5B%5D=48&rosen_id%5B%5D=49&rosen_id%5B%5D=51&rosen_id%5B%5D=52&rosen_id%5B%5D=53&rosen_id%5B%5D=54&rosen_id%5B%5D=55&rosen_id%5B%5D=56&rosen_id%5B%5D=57&rosen_id%5B%5D=58&rosen_id%5B%5D=59&rosen_id%5B%5D=62&rosen_id%5B%5D=63&rosen_id%5B%5D=64&rosen_id%5B%5D=81&rosen_id%5B%5D=84&rosen_id%5B%5D=86&rosen_id%5B%5D=95&rosen_id%5B%5D=102&rosen_id%5B%5D=106&rosen_id%5B%5D=126&rosen_id%5B%5D=127&rosen_id%5B%5D=130&rosen_id%5B%5D=131&rosen_id%5B%5D=132&rosen_id%5B%5D=134&rosen_id%5B%5D=135&rosen_id%5B%5D=136&rosen_id%5B%5D=137&rosen_id%5B%5D=140&rosen_id%5B%5D=143&rosen_id%5B%5D=145&rosen_id%5B%5D=147&rosen_id%5B%5D=148&rosen_id%5B%5D=155&rosen_id%5B%5D=157&rosen_id%5B%5D=158&rosen_id%5B%5D=159&rosen_id%5B%5D=311&rosen_id%5B%5D=312&rosen_id%5B%5D=519&rosen_id%5B%5D=522&rosen_id%5B%5D=526&rosen_id%5B%5D=549&rosen_id%5B%5D=555&rosen_id%5B%5D=567&todoufuken_cd=13&root_hidden=line&min_use_charge=0&max_use_charge=&min_area=0&max_area=&ekitoho=&chikunensu=' --compressed > {page}.log")
proc = subprocess.Popen(f"cat {page}.log | grep -Eo 'resultNum\">[0-9]+'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
total = int(out.decode('utf-8').strip().split('>')[-1])
pages = math.ceil(total / 10)

for page in range(2, pages + 1):
	os.system(f"curl 'https://chukai.setup-chintai.com/search/list.html' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Authorization: Basic bGl2ZW1heDE1MDA6bGl2ZW1heDE1MDA=' -H 'Origin: https://chukai.setup-chintai.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://chukai.setup-chintai.com/search/list.html' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'mode=shousai&page={page}&rosen_id%5B%5D=1&rosen_id%5B%5D=2&rosen_id%5B%5D=3&rosen_id%5B%5D=4&rosen_id%5B%5D=5&rosen_id%5B%5D=6&rosen_id%5B%5D=10&rosen_id%5B%5D=11&rosen_id%5B%5D=13&rosen_id%5B%5D=19&rosen_id%5B%5D=31&rosen_id%5B%5D=32&rosen_id%5B%5D=33&rosen_id%5B%5D=34&rosen_id%5B%5D=38&rosen_id%5B%5D=40&rosen_id%5B%5D=41&rosen_id%5B%5D=42&rosen_id%5B%5D=43&rosen_id%5B%5D=44&rosen_id%5B%5D=48&rosen_id%5B%5D=49&rosen_id%5B%5D=51&rosen_id%5B%5D=52&rosen_id%5B%5D=53&rosen_id%5B%5D=54&rosen_id%5B%5D=55&rosen_id%5B%5D=56&rosen_id%5B%5D=57&rosen_id%5B%5D=58&rosen_id%5B%5D=59&rosen_id%5B%5D=62&rosen_id%5B%5D=63&rosen_id%5B%5D=64&rosen_id%5B%5D=81&rosen_id%5B%5D=84&rosen_id%5B%5D=86&rosen_id%5B%5D=95&rosen_id%5B%5D=102&rosen_id%5B%5D=106&rosen_id%5B%5D=126&rosen_id%5B%5D=127&rosen_id%5B%5D=130&rosen_id%5B%5D=131&rosen_id%5B%5D=132&rosen_id%5B%5D=134&rosen_id%5B%5D=135&rosen_id%5B%5D=136&rosen_id%5B%5D=137&rosen_id%5B%5D=140&rosen_id%5B%5D=143&rosen_id%5B%5D=145&rosen_id%5B%5D=147&rosen_id%5B%5D=148&rosen_id%5B%5D=155&rosen_id%5B%5D=157&rosen_id%5B%5D=158&rosen_id%5B%5D=159&rosen_id%5B%5D=311&rosen_id%5B%5D=312&rosen_id%5B%5D=519&rosen_id%5B%5D=522&rosen_id%5B%5D=526&rosen_id%5B%5D=549&rosen_id%5B%5D=555&rosen_id%5B%5D=567&todoufuken_cd=13&root_hidden=line&min_use_charge=0&max_use_charge=&min_area=0&max_area=&ekitoho=&chikunensu=' --compressed > {page}.log")

line = []
station = []
duration = []
row_num_arr = []
for page in range(1, pages + 1):
	proc = subprocess.Popen(f"cat {page}.log | grep tdStation", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	row_num_arr += [int(int(re.search(r'[0-9]+', element).group(0)) / 2) for element in out.decode('utf-8').strip().split('\n')]
	proc = subprocess.Popen(f"cat {page}.log | grep -A9 tdStation", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	line += [element.replace('\t', '').replace('\n', '').split('<br />')[0].split('>')[-1] for element in out.decode('utf-8').split('--')]
	station += [element.replace('\t', '').replace('\n', '').split('<br />')[2] for element in out.decode('utf-8').split('--')]
	duration += [element.replace('\t', '').replace('\n', '').split('<br />')[-1] for element in out.decode('utf-8').split('--')]

doc_arr = []
room_arr = []
for page in range(1, pages + 1):	
	proc = subprocess.Popen(f"cat {page}.log | grep -A4 monthly-system", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	doc_arr += [re.search('(http|https)://[a-zA-Z0-9&;./?=_-]*', element).group(0) for element in out.decode('utf-8').strip().split('--')]
	room_arr += [element.split('\n')[-2].strip() for element in out.decode('utf-8').split('--')]

for index, num in enumerate(row_num_arr):
	os.system(f"mkdir -p '{line[index]}/{station[index]}'")
	for x in range(0, num):
		name = f"{duration[index]}_livemax_{index}_{room_arr[index + x]}"
		os.system(f"curl '{doc_arr[index + x]}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://chukai.setup-chintai.com/search/list.html' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --compressed > '{line[index]}/{station[index]}/{name}_doc.pdf'")
