
import os

print(os.getcwd())

import xmltodict, json

with open('./test/file.xml', 'r') as f:
    xml_string = f.read()

json_data = json.dumps(xmltodict.parse(xml_string))