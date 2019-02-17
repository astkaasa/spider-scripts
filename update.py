import json
import os
import subprocess
import datetime
import re
import time
import math
import sys
import glob
import zipfile
from bs4 import BeautifulSoup

with open('/home/ubuntu/data/data.json') as f:
    data = json.load(f)

today = datetime.date.today().isoformat()
today_new_list = glob.glob(f"/home/ubuntu/data/dates/{today}" + '/*.json')
today_keys_list = glob.glob(f"/home/ubuntu/data/keys/{today}" + '/*.json')

new_data = {}
for file_path in today_new_list:
    with open(file_path) as f:
        today_new = json.load(f)

    for key, value in today_new.items():
        new_data[key] = value
        data[key] = value

all_keys = []
for file_path in today_keys_list:
    with open(file_path) as f:
        today_keys = json.load(f)

    all_keys += today_keys

for key, value in data.items():
    if key not in all_keys:
        print(f"delete key: {key}")
        print(f"delete value: {data.pop(key)}")

with open(f"/home/ubuntu/data/data.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)

with open(f"/home/ubuntu/data/dates/{today}/{today}", "w") as f:
    json.dump(new_data, f, indent=2, sort_keys=False, ensure_ascii=False)

with open(f"/home/ubuntu/data/keys/{today}/{today}", "w") as f:
    json.dump(all_keys, f, indent=2, sort_keys=False, ensure_ascii=False)

def zipit(folders, zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(os.path.join(dirpath, filename), os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))
    zip_file.close()

docs_folders = []
images_folders = []
for key, value in new_data.items():
    path = f"{value['line']}/{value['station']}/{key}"
    docs_folders.append(f"/home/ubuntu/data/docs/{path}")
    images_folders.append(f"/home/ubuntu/data/images/{path}")

zipit(docs_folders, f"/home/ubuntu/data/zips/{today}_docs.zip")
zipit(images_folders, f"/home/ubuntu/data/zips/{today}_images.zip")
