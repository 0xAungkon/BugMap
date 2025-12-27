
import os

import base64

import xmltodict, json

with open('./tmp/test.xml', 'r') as f:
    xml_string = f.read()

json_data = xmltodict.parse(xml_string)

cleaned_json=[]

import base64, gzip, io

def decode_burp_response(b64):
    raw = base64.b64decode(b64)
    return raw.decode('utf-8', errors='ignore')

# Parsing Happen Here
for i in json_data['items']['item']:
    item={}
    item['time'] = i['time'] # Sat Dec 27 21:23:59 BDT 2025
    item['url'] = i['url']
    item['ip_address'] = i['host']['@ip']+':'+i['port']
    item['method'] = i['method']

    item['request'] = decode_burp_response(i['request']['#text'])
    item['protocol'] = i['protocol']

    item['response_status_code'] = i['status']
    item['response_mimetype'] = i['mimetype']
    item['response_length'] = i['responselength']
    item['response'] = decode_burp_response(i['response']['#text'])

    cleaned_json.append(item)
    


# Filters Applied Here
filterd_json = []

for i in cleaned_json:
    if "/api/" in i['url']:
        filterd_json.append(i)


# Formatting Happen Here
markdown = ''

for i in filterd_json:
    markdown += f"{i['method']} - {i['url']}\n\n"
    markdown += f"Request:\n\n"
    markdown += f"```\n"
    markdown += f"{i['request']}\n"
    markdown += f"```\n\n"
    markdown += f"Response:\n\n"
    markdown += f"```\n"
    markdown += f"{i['response']}\n"
    markdown += f"```\n\n"
    markdown += "---\n\n"

with open('./tmp/test.md', 'w') as f:
    f.write(markdown)
