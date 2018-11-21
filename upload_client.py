import requests as rq
import sys
import hashlib
import json
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
	key=RSA.construct(key_detail)
	pb=key.publickey() 
elif scheme=='2':
	#print('here')
	key=sys.argv[5]
	iv=sys.argv[6]
	#print(len(iv))
	#print(iv)
	aes=AES.new(key,AES.MODE_CBC,iv)
elif scheme=='3':
    key=sys.argv[5]
    key=key.encode('utf-8')
    d=des(key) 
	

username = sys.argv[1]
password = sys.argv[2]
with open(sys.argv[3],'rb') as rf:
    content1 = rf.read()
#print(scheme)
if scheme=='1':
	content=pb.encrypt(content1,32)
	content=content[0]
if scheme=='2':
	#print('here')
	content1=content1.decode('ISO-8859-1')
	extra=len(content1)%16
	if extra>0:
		content1=content1+(' '*(16-extra))
	content1 = content1.encode('ISO-8859-1') 
	content=aes.encrypt(content1)
if scheme=='3':
	content1=content1.decode('ISO-8859-1')
	extra=len(content1)%8
	if extra>0:
		content1=content1+(' '*(8-extra))
	content1 = content1.encode('ISO-8859-1') 
	content=d.encrypt(content1)

#print(content)
sendcon = content.decode('ISO-8859-1')
#print()
#print(sendcon)
md5sum = hashlib.md5(content).hexdigest()
r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':sys.argv[3], 'content':sendcon, 'md5':md5sum})
rld = json.loads(r.content.decode())
while rld['checksum'] == 'false':
    r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':sys.argv[3], 'content':sendcon, 'md5':md5sum})
    rld = json.loads(r.content.decode())
