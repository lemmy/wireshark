#!/usr/bin/python3

import os
import re

import gzip
import json

def pageCount(data, rfc):
    for page in data:
        if page['doc_id'] == rfc:
            return page['page_count']
    return 0

print('RFC,Page_Count,File,LOC,RFC_URL,File_URL')

with gzip.open('ietf.json.gz', 'rb') as gzipped_file:
    file_content = gzipped_file.read()
    json_text = file_content.decode('utf-8')
    ietf = json.loads(json_text)    

# with open('ietf.json', 'r') as json_file:
#     ietf = json.load(json_file)

for filename in os.listdir('.'):
    if filename.startswith('') and filename.endswith('.h'):
        with open(filename, 'r') as header:
            lines = header.readlines()
        if os.path.exists(filename.replace(".h", ".c")):
            with open(filename.replace(".h", ".c"), 'r') as impl:
                lines += impl.readlines()
        rfcs = set()
        for line in lines:
            matches = re.search(r'([Rr][Ff][Cc])\s?([0-9]+)', line)
            if matches:
                rfcs.add(matches.group(1).upper() + matches.group(2).zfill(4))
        for rfc in rfcs:
            print(f'{rfc},{pageCount(ietf, rfc)},{filename.replace(".h", "")},{len(lines)},https://tools.ietf.org/html/{rfc},https://github.com/lemmy/wireshark/blob/master/epan/dissectors/{filename},https://github.com/lemmy/wireshark/blob/master/epan/dissectors/{filename.replace(".h", ".c")}')