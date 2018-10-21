import requests as rq
import sys
import hashlib
import json

username = sys.argv[1]
password = sys.argv[2]
with open(sys.argv[3],'rb') as rf:
    content = rf.read()
sendcon = content.decode('ISO-8859-1')
md5sum = hashlib.md5(content).hexdigest()
r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':sys.argv[3], 'content':sendcon, 'md5':md5sum})
rld = json.loads(r.content.decode())
while rld['checksum'] == 'false':
    r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':sys.argv[3], 'content':sendcon, 'md5':md5sum})
    rld = json.loads(r.content.decode())
