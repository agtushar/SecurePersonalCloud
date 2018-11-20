import requests as rq
import json
import hashlib
import sys
import os
import subprocess
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import pyDes
from pyDes import des

res = rq.post('http://127.0.0.1:8000/storage/md5s/', data={'name':sys.argv[1], 'password':sys.argv[2]})

jsond = json.loads(res.content.decode())
#print(jsond)
comm = 'find '+sys.argv[3]+' -type f'
files = subprocess.check_output(comm, shell=True).decode().split('\n')
print(files)
for item in files[:-1]:
    if item not in jsond.keys():
        comm = 'python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]+' '+sys.argv[7]
        print('Uploading new ',item)	
        os.system(comm)
for item in jsond.keys():
    if item not in files:
        var = input("File exists in server. Want to download? 'N' for no\n")
        if var == 'N':
            res = rq.post('http://127.0.0.1:8000/storage/deletefile/', data={'name':sys.argv[1],'password':sys.argv[2],'filename':item})
            print('Deleting ',item)
        else:
            os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]+' '+sys.argv[7])
            print('Downloading exclusive ',item)
    else:
        with open(item,'rb') as rf:
            cont = rf.read()
            conte = cont.decode('ISO-8859-1')
            if sys.argv[4]=='1':
                e=int(sys.argv[6])
                d=int(sys.argv[7])
                n=int(sys.argv[5])
                key_detail=(n,e,d)
                key=RSA.construct(key_detail)
                pb=key.publickey() 
                cont=pb.encrypt(cont,32)
                cont=cont[0] 

            if sys.argv[4]=='2':
                key=sys.argv[5]
                iv=sys.argv[6]
                aes=AES.new(key,AES.MODE_CBC,iv)
                extra=len(conte)%16
                if extra>0:
                    conte=conte+(' '*(16-extra))
                conte = conte.encode('ISO-8859-1') 
                cont=aes.encrypt(conte)
 
            if sys.argv[4]=='3':
                key=sys.argv[5]
                key=key.encode('utf-8')
                d=des(key)
                extra=len(conte)%8
                if extra>0:
                    conte=conte+(' '*(8-extra))
                conte = conte.encode('ISO-8859-1') 
                cont=d.encrypt(conte)

            md5 = hashlib.md5(cont).hexdigest()
            
            #print(md5)
            #print(jsond[item]) 

            if not md5 == jsond[item]:
                var = input("Files exist locally and at server. '1' for server copy, '2' for local copy "+item+"\n")
                if var == '1':
                    os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]+' '+sys.argv[7])
                    print('Downloading overwrite ',item)
                else:
                    os.system('python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]+' '+sys.argv[7])
                    print('Uploading overwrite ',item)
