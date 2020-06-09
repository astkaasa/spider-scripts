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

procs = []
ids = []

for page in range(0, 3819):
    proc = subprocess.Popen(f"curl 'https://learning.oreilly.com/api/v2/search/?query=&page={page}&formats=book' -H 'authority: learning.oreilly.com' -H 'cache-control: max-age=0' -H 'dnt: 1' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3942.0 Safari/537.36' -H 'sec-fetch-user: ?1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'sec-fetch-site: none' -H 'sec-fetch-mode: navigate' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7' -H 'cookie: BrowserCookie=303105da-7553-46fc-b5fb-fac789590311; _gcl_au=1.1.83214345.1570675908; _vwo_uuid_v2=D6D25D2AC0726CA2B3468A799B3089C06|d43041b1c71da8cd8eccb18648c0289b; recently-viewed=%5B%229781932394887%22%2C%229781617293726%22%2C%229781491924570%22%5D; groot_sessionid=u835xlhxpyyi9dygcithrs34wk0y0ezk; sessionid=3q0yhke91ymcvs3hzp3411913dnhd93s; _ga=GA1.2.1466215930.1571215626; logged_in=y; orm-rt=fe6b09d8c87b40cdb4f6d782a64de22c; csrfsafari=PsuJGxUGrxJAHFXNZelevkGswyGLTvVKD9dTRYfucHyB5WJn0vFlNSoyu6n0VN6c; orm-jwt=eyJhbGciOiAiUlMyNTYifQ.eyJhY2N0cyI6IFsiYWQyNjA1ZDMtMTRhMC00YmM0LWI4MmQtNmI1ZWYyMTU4YmZlIl0sICJlaWRzIjogeyJoZXJvbiI6ICI0MjViMDY2My03MDE0LTRhZWQtYTY2OS00NjE3MWQ2MzFjMWYifSwgImVudiI6ICJwcm9kdWN0aW9uIiwgImV4cCI6IDE1NzEzNzU0NTgsICJpbmRpdmlkdWFsIjogZmFsc2UsICJwZXJtcyI6IHsiYXBpZGMiOiAidiIsICJhc2lnbiI6ICJ2IiwgImNuZnJjIjogInYiLCAiY3ByZXgiOiAidiIsICJjc3N0ZCI6ICJ2IiwgImVwdWJzIjogInYiLCAibHJwdGgiOiAidiIsICJudGJrcyI6ICJ2IiwgIm9yaW9sIjogInYiLCAicGx5bHMiOiAidiIsICJ1c2FnZSI6ICJjIiwgInVzcnBmIjogImV2IiwgInZpZGVvIjogInYifSwgInN1YiI6ICI3ZTYyOWQxMS1hOWQ0LTQ1ZmUtOGFkNy1lYzc4NjRhMjc5M2QifQ.VUA8EZwWa5TQw89wL0gkLqr41M43tFWcD8aKhP1pFh3oWQnAB_98rJsuFHkuHMttGPJp9jVexnjPB_kINhMJNbcdj78_FIHaCgkCX-NAibtNX6lQZ7S8dmfb7yk4IDSt8K7WzRdCKjrg8yBHMIvArfP5JL9YV45et1xwMBssKpI' --compressed", stdout=subprocess.PIPE, shell=True)
    procs.append(proc)

for p in procs:
    (out, err) = p.communicate()
    for item in json.loads(out.decode('utf-8').strip())["results"]:
        ids.append(item["archive_id"])

print(ids)
