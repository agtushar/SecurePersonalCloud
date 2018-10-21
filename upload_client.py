import requests as rq
import sys

print(sys.argv[1])
username = sys.argv[1]
password = sys.argv[2]
md5sum = sys.argv[3]
with open(sys.argv[3],'rb') as rf:
    content = rf.read()
sendcon = content.decode('ISO-8859-1')
r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':sys.argv[3], 'content':sendcon, 'checksum':md5sum})
