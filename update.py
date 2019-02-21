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
    value["deleted"] = key not in all_keys

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

folders = []
# images_folders = []
for key, value in new_data.items():
    path = f"{value['room_size']}/{value['line']}/{value['station']}/{key}"
    folders.append(f"/home/ubuntu/data/rooms/{path}")
    # images_folders.append(f"/home/ubuntu/data/images/{path}")

zipit(folders, f"/home/ubuntu/data/zips/{today}.zip")
# zipit(images_folders, f"/home/ubuntu/data/zips/{today}_images.zip")
