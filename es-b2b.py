import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

# hiro-corporation;47DB45Z;AC4VVL4MGL
# am-bition;46NW3M5;Q747QV2MGK
# trust-advisers;40WS3H2;G44FL25MGM
# meiwa-chukai;51H64KW;FD4HCU3MGL
# tfd;19NV37T;JZ37YA5MGS
# sfit-pm;41AZ3M6;J5433Q2MGL
# aml-chintai;538E4PA;BF4HCZ5MGL
# reloko-tokyo;54AB4MZ;P74KRZ2MGN
# stageplan;38Z843V;ZG4MZ54MGL
# itc-uc;528P4MY;7F43554MGL
site, username, password = sys.argv[1].split(';')

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}/es-b2b"
os.system(f"mkdir -p {path}")
os.chdir(path)

proc = subprocess.Popen(f"curl -c - 'https://{site}.es-b2b.com/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --compressed | awk '$6 ~ /JSESSIONID/ {{print $7}}'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth1 = out.decode('utf-8').strip()

os.system(f"curl -L 'https://{site}.es-b2b.com/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}' --compressed")
os.system(f"curl -L 'https://{site}.es-b2b.com/' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}' --compressed")

proc = subprocess.Popen(f"curl -c - 'https://{site}.es-b2b.com/?wicket:interface=:2:signInPanel:signInForm::IFormSubmitListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://{site}.es-b2b.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/signIn' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}' --data 'signInPanel_signInForm%3Ahf%3A0=&username={username}&x=40&y=52&password={password}' --compressed", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth2 = out.decode('utf-8').split('\t')[-1].strip()

os.system(f"curl 'https://{site}.es-b2b.com/search/line' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --compressed > {site}.log")

proc = subprocess.Popen(f"cat {site}.log | grep 'form action=\"/?wicket:interface=:' | grep -Eo '[0-9]+'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
interface = int(out.decode('utf-8').split('\n')[0])

proc = subprocess.Popen(f"cat {site}.log | grep -Eo 'lineCheckBox[0-9]+' | uniq | wc -l", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
line_total = int(out.decode('utf-8').strip())

line_str = ''
for x in range(0, line_total):
	line_str += f"lineSelectGroup=check{x}&"

os.system(f"curl 'https://{site}.es-b2b.com/?wicket:interface=:{interface}:form::IFormSubmitListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://{site}.es-b2b.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/search/line' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --data 'topSubmitButton=x&{line_str}hopeConditionPanel%3ArentLowerCode=&hopeConditionPanel%3ArentUpperCode=&hopeConditionPanel%3AusePartAreaLowerCode=&hopeConditionPanel%3AusePartAreaUpperCode=&hopeConditionPanel%3AwalkFromStationLowerCode=&hopeConditionPanel%3AwalkFromStationUpperCode=&hopeConditionPanel%3AadArea%3AadLowerCode=&hopeConditionPanel%3AadArea%3AadUpperCode=' --compressed")
interface += 1

proc = subprocess.Popen(f"curl -L 'https://{site}.es-b2b.com/?wicket:interface=:{interface}:form::IFormSubmitListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://{site}.es-b2b.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/?wicket:interface=:6::' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --data 'numChangeButton=x&rowsPerPage=50&hopeConditionPanel%3ArentLowerCode=&hopeConditionPanel%3ArentUpperCode=&hopeConditionPanel%3AusePartAreaLowerCode=&hopeConditionPanel%3AusePartAreaUpperCode=&hopeConditionPanel%3AwalkFromStationLowerCode=&hopeConditionPanel%3AwalkFromStationUpperCode=&hopeConditionPanel%3AadArea%3AadLowerCode=&hopeConditionPanel%3AadArea%3AadUpperCode=' --compressed | grep 'form action=\"/?wicket:interface=:' | grep -Eo '[0-9]+'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
interface = int(out.decode('utf-8').split('\n')[0])

page = 0
os.system(f"curl 'https://{site}.es-b2b.com/?wicket:interface=:{interface}::' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/search/line' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --compressed > {site}_{page}.log")

proc = subprocess.Popen(f"cat {site}_{page}.log | grep '検索結果：'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
total = int(re.search(r'[0-9]+', out.decode('utf-8')).group(0))
pages = math.ceil(total / 50)
index = 0
for index in range(0 + page * 50, (page + 1) * 50 if total > (page + 1) * 50 else total):
	os.system(f"curl 'https://{site}.es-b2b.com/?wicket:interface=:{interface}:form:propertyListView:{index}:row:manageBeltPdfButton::ILinkListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --compressed > {site}_{index}.pdf")
for page in range(1, pages):
	os.system(f"curl 'https://{site}.es-b2b.com/?wicket:interface=:{interface}:form:topPageNavi:navigation:{page}:pageLink::ILinkListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://{site}.es-b2b.com/?wicket:interface=:{interface}::' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --compressed > {site}_{page}.log")
	for index in range(0 + page * 50, (page + 1) * 50 if total > (page + 1) * 50 else total):
		os.system(f"curl 'https://{site}.es-b2b.com/?wicket:interface=:{interface}:form:propertyListView:{index}:row:manageBeltPdfButton::ILinkListener' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3543.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth1}; b2bLogedInTicket={auth2}' --compressed > {site}_{index}.pdf")

line_arr = []
station_arr = []
duration_arr = []
for page in range(0, pages):
	proc = subprocess.Popen(f"cat {site}_{page}.log | grep vicinityInfo", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	line_arr += [element.strip().split('<span>')[2].split('</span>')[0] for element in out.decode('utf-8').strip().split('\n')]
	station_arr += [element.strip().split('<span>')[1].split('</span>')[0] for element in out.decode('utf-8').strip().split('\n')]
	duration_arr += [element.strip().split('<span>')[3].split('</span>')[0] for element in out.decode('utf-8').strip().split('\n')]

arr = []
for page in range(0, pages):
	proc = subprocess.Popen(f"cat {site}_{page}.log | grep -Eo 'propertyFullId/[0-9]+'", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	arr += out.decode('utf-8').strip().split('\n')

for index, item in enumerate(arr):
	url = "https://images.es-e-bukken.com/gpool/0/"
	number = item.split('/')[-1].zfill(31)
	for x in range(0, 10):
		url = url + number[3 * x + 1: 3 * x + 4] + "/"
	url = url + number
	name = f"{line_arr[index]}/{station_arr[index]}/{duration_arr[index]}_{site}_{index}"
	os.system(f"mkdir -p '{name}'")
	os.system(f"mv {site}_{index}.pdf '{name}/doc.pdf'")
	os.system(f"t=0\ni=1\nwhile [ $i -le 200 ]\ndo\n\tif [ $t -gt 10 ]\n\tthen\n\t\tbreak\n\tfi\n\tif wget -O \"{name}/$i.jpg\" \"{url}_$i.jpg\"\n\tthen\n\t\ti=$((i+1))\n\telse\n\t\tt=$((t+1))\n\t\trm \"{name}/$i.jpg\"\n\t\ti=$((i+1))\n\tfi\ndone")
