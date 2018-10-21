import requests as rq
import sys
import json
import os

username = sys.argv[1]
password = sys.argv[2]
res = rq.post('http://127.0.0.1:8000/storage/download/', data={'name':username, 'password':password})
rldata = json.loads(res.content.decode())
for key, value in rldata.items():
    directory = './temp'+key
    directory = os.path.dirname(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('temp'+key,'wb') as wf:
        wf.write(bytes(rldata[key], encoding='ISO-8859-1'))

