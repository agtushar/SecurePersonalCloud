import requests as rq
import sys
import json
import os
import hashlib

username = sys.argv[1]
password = sys.argv[2]
res = rq.post('http://127.0.0.1:8000/storage/download1/', data={'name':username, 'password':password, 'filename':sys.argv[3]})
rldata = json.loads(res.content.decode())
md5 = hashlib.md5(rldata[sys.argv[3]][0].encode('ISO-8859-1')).hexdigest()
if 'userFail' in rldata.keys():
    sys.exit()
while md5 != rldata[sys.argv[3]][1]:
    res = rq.post('http://127.0.0.1:8000/storage/download1/', data={'name':username, 'password':password, 'filename':sys.argv[3]})
    rldata = json.loads(res.content.decode())
    md5 = hashlib.md5(rldata[sys.argv[3]][0]).hexdigest()

for key, value in rldata.items():
    directory = key
    directory = os.path.dirname(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(key,'wb') as wf:
        wf.write(bytes(rldata[key][0], encoding='ISO-8859-1'))
