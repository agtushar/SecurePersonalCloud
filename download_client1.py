import requests as rq
import sys
import json
import os
import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
import pyDes
from pyDes import des 

scheme=sys.argv[4]
if scheme=='1':
    key=sys.argv[5]
    arc=ARC4.new(key)  
elif scheme=='2':
    key=sys.argv[5]
    iv=sys.argv[6]
    aes=AES.new(key,AES.MODE_CBC,iv)
elif scheme=='3':
    key=sys.argv[5]
    key=key.encode('utf-8')
    d=des(key) 

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
        var=rldata[key][0].encode('ISO-8859-1')
        c=''
        if scheme=='1':
            decd=arc.decrypt(var)
            wf.write(decd) 
        elif scheme=='2': 
            decd=aes.decrypt(var)
            #print(decd)
            y=decd.decode('ISO-8859-1')   
            c=y.rstrip()
            wf.write(c.encode('ISO-8859-1'))
            #print(c.encode('ISO-8859-1'))
            #print(c)
            #with open('down.txt','wb') as wf:
            #    wf.write(content1.encode('ISO-8859-1'))
        elif scheme=='3': 
            decd=d.decrypt(var)
            y=decd.decode('ISO-8859-1')
            c=y.rstrip()
            wf.write(c.encode('ISO-8859-1'))

