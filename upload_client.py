import requests as rq
import sys
import hashlib
import json
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

	#print(len(content1))
 #print(scheme)
if scheme=='1':
	content=arc.encrypt(content1)
if scheme=='2':
	#with open('up.txt','wb') as wf:
	#	wf.write(content1)
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
	#print("Encrypting")
	content=d.encrypt(content1)

#print(content)
sendcon = content.decode('ISO-8859-1')
#print()
#print(sendcon)
md5sum = hashlib.md5(content).hexdigest()
with open('direct_name', 'r') as rf:
	strtS = rf.read().strip('\n')
lis2 = strtS.split('/')
relPath = lis2[-1]+sys.argv[3][len(strtS):]
r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':relPath, 'content':sendcon, 'md5':md5sum})
rld = json.loads(r.content.decode())
while rld['checksum'] == 'false':
	r = rq.post('http://127.0.0.1:8000/storage/upload/', data={'name':username, 'password':password, 'filename':relPath, 'content':sendcon, 'md5':md5sum})
	rld = json.loads(r.content.decode())
