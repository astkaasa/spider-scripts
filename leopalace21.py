import json
import os
import subprocess
import datetime
import re
import time
import math
import sys

with open('/home/ubuntu/leopalace21.json') as f:
	data = json.load(f)

today = datetime.date.today().isoformat()
proc = subprocess.Popen("curl -c - 'https://www.leopalace21.com/apps/tradeCondition/logonAction.do' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'actionType=LOGON&id=262782695z%40gmail.com&password=123456' --compressed | awk '$0 ~ /JSESSIONID/ {print $7}'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth = out.decode('utf-8').strip()

for company, value in data.items():
	for line, line_id in value.items():
		path = f"/home/ubuntu/{today}/leopalace21/{company}/{line}"
		os.system(f"mkdir -p {path}")
		os.chdir(path)
		arr = []
		os.system(f"curl 'https://www.leopalace21.com/apps/tradeCondition/conditionAction.do' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://www.leopalace21.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.leopalace21.com/apps/tradeCondition/conditionAction.do' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth}; ' --data 'actionType=SEARCHBUKKEN&searchType=ENSEN&localCitySelectionString=&ensenSelectionString={line_id}&ekiSelectionString=&pageNo=1&apnos=&sortItem=2&lineCount=1000&sortItem2=2&lineCount2=1000&monkan=0&rank1Selection=&rank2Selection=&nyukyoJikiSelection=&mensekiFromSelection=&mensekiToSelection=&sinceYearSelection=&keyword=' --compressed > all.log")
		with open('all.log', encoding='CP932') as f:
			for line in f.readlines():
				if '<p class="photo"><a href="javascript:detail(' in line:
					arr.append(re.search(r'[0-9]+', line).group(0))

		station_arr = []
		duration_arr = []
		proc = subprocess.Popen(f"cat all.log | iconv -f cp932 -t utf-8 | grep -A1 '</em> から'", stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		station_arr = [element.strip().split('\n')[0].strip().split('/ ')[1].split('</em>')[0].strip() for element in out.decode('utf-8').split('--')]
		duration_arr = [element.strip().split('\n')[1].strip().split('</span>/ ')[-1].replace('<li>', '').replace('</li>', '') for element in out.decode('utf-8').split('--')]


		for index, apt_id in enumerate(arr):
			details = {}
			os.system(f"curl 'https://www.leopalace21.com/apps/tradeCondition/conditionAction.do' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: https://www.leopalace21.com' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.leopalace21.com/apps/tradeCondition/conditionAction.do' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: JSESSIONID={auth}; ' --data 'actionType=BUKKENDETAIL&searchType=ENSEN&localCitySelectionString=&ensenSelectionString={line_id}&ekiSelectionString=&pageNo=1&apno={apt_id}&apnos=&sortItem=2&lineCount=1000&sortItem2=2&lineCount2=1000&monkan=0&rank1Selection=&rank2Selection=&nyukyoJikiSelection=&mensekiFromSelection=&mensekiToSelection=&sinceYearSelection=&keyword=' --compressed > {apt_id}.log")
			proc = subprocess.Popen(f"cat {apt_id}.log | iconv -f cp932 -t utf-8 | grep -a 'www.leopalace21.com/app/image' | grep -Eo '(http|https)://[a-zA-Z0-9&;./?=_-]*' | uniq", stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			images = out.decode('utf-8').replace("amp;", "").split('\n')
			images.pop()

			proc = subprocess.Popen(f"cat {apt_id}.log | iconv -f cp932 -t utf-8 | grep -a 'name=\"memberRoom\"' | grep -Eo '[0-9]+'", stdout=subprocess.PIPE, shell=True)
			(out,err) = proc.communicate()
			rooms = out.decode('utf-8').split('\n')
			rooms.pop()


			name = f"{station_arr[index]}/{duration_arr[index]}_leopalace21_{apt_id}"
			os.system(f"mkdir -p '{name}'")
			for image_url in images:
				image_name = re.search(r'IMAGE=[a-zA-Z0-9_]+', image_url).group(0).replace("IMAGE=", "").lower()
				os.system(f"wget -O '{name}/{image_name}.jpeg' '{image_url}'")

			for room in rooms:
				os.system(f"curl 'https://www.leopalace21.com/apps/tradeCondition/createPDFAction.do' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: https://www.leopalace21.com' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.leopalace21.com/apps/tradeCondition/conditionAction.do' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,ja;q=0.6' -H 'Cookie: JSESSIONID={auth}' --data 'actionType=BUKKENDETAILPDF&searchType=LEO&apno={apt_id}&membergonos={room}&flatgonos=&kikans=&statuss=&specialOff=false&code=&reikinZero=true&grayScale=false&replace=false&x=&y=&scale=0' --compressed > '{name}/{room}_doc.pdf'")
