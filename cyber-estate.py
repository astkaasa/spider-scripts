import json
import os
import subprocess
import datetime
import re
import time
import math
import sys
from bs4 import BeautifulSoup

# 813053;262782695z;shimada100
# 113055;7894561233;3216549877
# 813013;101927;6102
site, username, password = sys.argv[1].split(';')

today = datetime.date.today().isoformat()
path = f"/home/ubuntu/{today}"
os.system(f"mkdir -p {path}")
os.chdir(path)

proc = subprocess.Popen(f"curl -c - 'http://mediation.cyber-estate.jp/mediation/login.asp?ggid={site}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://mediation.cyber-estate.jp' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' --data 'txtLoginId={username}&txtLoginPass={password}' --compressed | awk '$6 ~ /^med$/ {{print $7}}'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
auth = out.decode('utf-8').strip()

proc = subprocess.Popen(f"curl 'https://mediation.cyber-estate.jp/mediation/search/search_top.asp?ggid={site}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3603.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://mediation.cyber-estate.jp/mediation/login.asp?ggid={site}&to=1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: med={auth}' --compressed | grep -Eo \"funcSearchStation\\(true, '[0-9_]+\"", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
search_str = '|'.join([element.strip().split('\'')[1] for element in out.decode('utf-8').strip().split('\n')])

os.system(f"curl 'http://mediation.cyber-estate.jp/mediation/main/main_list.asp?lat=0&lng=0&ggid={site}&sbt=1&scdiv=2&towndiv=2&area=&scarea=&stndiv=2&route={search_str}&sc1=0&sc2=00000&sc3=0&sc4=000000000&sc5=00000&sc6=1&sc7=1&sc8=1&sc9=1&sc10=000000000000000000000000000000000000000000000000000000000000&sc11=000000000000000&sc12=000000000000000&sc13=0&sc14=0&sc15=&sc16=&sc17=&sc18=&sc19=0&sc20=0&swlat=0&nelat=0&swlng=0&nelng=0&scgid=0&scbid=0&pref=0&city=0&station=A&tcd=0&SortKBN=9&dp=1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3603.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: med={auth}' --compressed > cyber-estate_{site}_1.log")

proc = subprocess.Popen(f"cat cyber-estate_{site}_1.log | grep -Eo '<span class=\"red\">[0-9]+</span>'", stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
total = int(re.search(r'[0-9]+', out.decode('utf-8')).group(0))

pages = math.ceil(total / 60)
pages = 1
for x in range(2, pages + 1):
    os.system(f"curl 'http://mediation.cyber-estate.jp/mediation/main/main_list.asp?lat=0&lng=0&ggid={site}&sbt=1&scdiv=2&towndiv=2&area=&scarea=&stndiv=2&route=1_91|1_93|1_95|1_103|1_105|1_110|1_194|94_3003|130_429|130_437|130_440|130_442|130_443|137_863|137_865|137_866|137_871|160_873|168_586|168_587|168_589|171_882|171_885|171_889|171_890|171_891|171_893|171_2009|172_564|172_576|172_577|172_579|172_580|172_582|172_583|172_584|172_585|173_830|173_843|173_848&scroute=1_91|1_93|1_95|1_103|1_105|1_110|1_194|130_429|130_437|130_440|130_442|130_443|172_564|172_576|172_577|172_579|172_580|172_582|172_583|172_584|172_585|168_586|168_587|168_589|173_830|173_843|173_848|137_863|137_865|137_866|137_871|160_873|171_882|171_885|171_889|171_890|171_891|171_893|171_2009|94_3003&sc1=0&sc2=00000&sc3=0&sc4=000000000&sc5=00000&sc6=1&sc7=1&sc8=1&sc9=1&sc10=000000000000000000000000000000000000000000000000000000000000&sc11=000000000000000&sc12=000000000000000&sc13=0&sc14=0&sc15=&sc16=&sc17=&sc18=&sc19=0&sc20=0&swlat=0&nelat=0&swlng=0&nelng=0&scgid=0&scbid=0&pref=0&city=0&station=A&tcd=0&SortKBN=9&dp={x}' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: med={auth}' --compressed > cyber-estate_{site}_{x}.log")

arr = []
for x in range(1, pages + 1):
    proc = subprocess.Popen(f"cat cyber-estate_{site}_{x}.log | grep -Eo 'bid=\"[0-9]+\" hid=\"[0-9]+\"'", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    items = out.decode('utf-8').split('\n')
    items.pop()
    for item in items:
        arr.append(re.findall(r'[0-9]+', item))

data = []
for x in arr:
    item = {}
    item["src_id"] = f"{x[0]}_{x[1]}"
    item["date"] = today
    item["site"] = f"cyber-estate_{site}"
    os.system(f"curl 'http://mediation.cyber-estate.jp/mediation/main/detail_heya.asp?ggid={site}&gid={site}&bid={x[0]}&hid={x[1]}&sbt=1&pagekb=2&pinst=1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: med={auth}' --compressed > cyber-estate_{site}_{x[0]}_{x[1]}.log")
    
    with open(f"cyber-estate_{site}_{x[0]}_{x[1]}.log") as f:
        soup = BeautifulSoup(f, 'html5lib')

    for br in soup.find_all("br"):
        br.replace_with("\n" + br.text)

    table = soup.find("table", { "id" : "detail_pickup" })

    headers = []
    for td in table.findAll("tr")[1].findAll("td"):
        headers += [e.strip() for e in re.split(r"\n+", td.text.strip())]

    texts = []
    for td in table.findAll("tr")[2].findAll("td"):
        texts += [e.strip() for e in re.split(r"\n+", td.text.strip())]

    details = {}
    for i, header in enumerate(headers):
        details[header] = texts[i]

    # for tr in soup.find("div", { "id" : "detail_info" }).find("table").findAll("tr", recursive=False):
    #     tds = tr.findAll("td", recursive=False)
    #     for i, td in enumerate(tds):
    #         if i % 2 == 1:
    #             details[tds[i - 1].text] = re.split(r"\s+", tds[i].text.strip())

    images = {}
    for li in soup.find('div', {'id': 'detail_pic'}).findAll('li'):
        re.sub(r"\s+", "", li.text, flags=re.UNICODE)
        images[re.sub(r"\s+", "", li.text, flags=re.UNICODE)] = li.find('img')['src']

    # '交通': 'ＪＲ京浜東北・根岸線 川口'
    item["line"] = re.split(r'\s+', details['交通'])[0]
    item["station"] = re.split(r'\s+', details['交通'])[1].split('／')[0]
    item["duration"] = re.split(r'\s+', details['交通'])[1].split('／')[1] if len(re.split(r'\s+', details['交通'])[1].split('／')) > 1 else ''
    item["images"] = images
    item["details"] = details

    name = f"cyber-estate_{site}_{x[0]}_{x[1]}"
    os.system(f"mkdir -p '{name}'")

    os.system(f"curl 'http://mediation.cyber-estate.jp/mediation/report/zumen_zip.asp?ggid={site}&sbt=1&gid={site}&bid={x[0]}&hid={x[1]}&hyadtl=1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3541.0 Safari/537.36' -H 'DNT: 1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5' -H 'Cookie: med={auth}' --compressed > '{name}/doc.pdf'")

    os.chdir(name)
    for image_name, image_url in images.items():
        os.system(f"wget -o /dev/null -qO '{image_name}.jpg' '{image_url}'")

    data.append(item)
    os.chdir(path)

with open(f"/home/ubuntu/{today}/cyber-estate_{site}.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)