import requests as rq
import sys
import json
import os
import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import pyDes
from pyDes import des 

scheme=sys.argv[4]
if scheme=='1':
    e=int(sys.argv[6])
    d=int(sys.argv[7])
    n=int(sys.argv[5])
    key_detail=(n,e,d)
    key_made=RSA.construct(key_detail)
    pb=key_made.publickey() 
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
    with open(key,'w') as wf:
        var=rldata[key][0].encode('ISO-8859-1')
        print(type(var))
        c=''
        if scheme=='1':
            tobe=key_made.decrypt(var)
            c=tobe.decode('ISO-8859-1')
        elif scheme=='2': 
            decd=aes.decrypt(var)
            #print(decd)
            y=decd.decode('ISO-8859-1')   
            #print(y)
            c=y.rstrip()
        elif scheme=='3':
            decd=d.decrypt(var)
            y=decd.decode('ISO-8859-1')
            c=y.rstrip()
        wf.write(c)

