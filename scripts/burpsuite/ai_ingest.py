import base64
import xmltodict
import json

def decode_burp_response(b64):
    raw = base64.b64decode(b64)
    return raw.decode('utf-8', errors='ignore')

def ingest_burp_xml(xml_string):
    json_data = xmltodict.parse(xml_string)
    
    cleaned_json=[]

    # Parsing Happen Here
    # Handle single item case vs list of items
    items = json_data.get('items', {}).get('item', [])
    if isinstance(items, dict):
        items = [items]
        
    for i in items:
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
        # Check if response exists and has text
        if i.get('response') and '#text' in i['response']:
             item['response'] = decode_burp_response(i['response']['#text'])
        else:
             item['response'] = ""

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
    
    return markdown
