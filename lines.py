import json
import os
import subprocess
import datetime
import re
import time
import math
import sys
import argparse

with open('/home/ubuntu/lines.json') as f:
    lines = json.load(f)

for name, alias in lines.items():
    arr = name.split('（')
    if '線（' in name:
        alias.append(arr[0])
        alias.append(arr[0][:-1])
    else:
        alias.append(arr[0] + '線')
        alias.append(arr[0])

with open("/home/ubuntu/lines.json", "w") as f:
    json.dump(lines, f, indent=2, sort_keys=True, ensure_ascii=False)
