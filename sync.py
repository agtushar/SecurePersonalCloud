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
from Crypto.Cipher import ARC4
import blowfish
import time
import threading

#a=time.time()
sc=sys.argv[4]
flag=1
d=0
def helper():
    #print('here')
    r = rq.post('http://127.0.0.1:8000/storage/end/', data={'name':sys.argv[1], 'password':sys.argv[2]})
    #print('here')
    os._exit(1)
#print(sys.argv[1])
#print(sys.argv[2])
if sc!='status':
    r = rq.post('http://127.0.0.1:8000/storage/begin/', data={'name':sys.argv[1], 'password':sys.argv[2]})
    rld = json.loads(r.content.decode())
    if rld['syncing'] == 'true':
        print('Another sync in progress')
        flag=0



if flag==1:
    res = rq.post('http://127.0.0.1:8000/storage/md5s/', data={'name':sys.argv[1], 'password':sys.argv[2]})

    #print(sys.argv[5])
    #print(sys.argv[6])
    #print(sys.argv[7])

    jsond = json.loads(res.content.decode())
    #print(jsond)
    comm = 'find '+sys.argv[3]+' -type f'
    files = subprocess.check_output(comm, shell=True).decode().split('\n')
    with open('direct_name', 'r') as rf:
        strtS = rf.read().strip('\n')
    lis2 = strtS.split('/')
    bstrt = strtS[:-len(lis2[-1])]
    ce=''
    se=''
    csm=''
    cs=''
    for item in files[:-1]:
        if item[len(bstrt):] not in jsond.keys():
            item="\""+item+"\""
            if sc=='1':
                comm = 'python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]
            elif sc=='2':
                comm = 'python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]
            elif sc=='3':
                comm = 'python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]
            elif sc=='status':
                ce=ce+item[len(bstrt):]+'\n'
            if sc!='status':
                print('Uploading new ',item)
                os.system(comm)
    nfiles=[]
    for item in jsond.keys():
        nfiles.append(bstrt+item)
    for item in nfiles:
        if item not in files:
            if sc=='status':
                se=se+item[len(bstrt):]+'\n'
            else: 


                timeout = 30
                t = threading.Timer(timeout, helper)
                t.start()
                prompt = "File exists in server. Want to download? 'N' for no\n"
                var = input(prompt) 
                t.cancel() 

                #print('UU')
                if var is None:
                    res = rq.post('http://127.0.0.1:8000/storage/lockfree/', data={'name':sys.argv[1],'password':sys.argv[2]})
                #var = input("File exists in server. Want to download? 'N' for no\n")
                #print(time.time()-a)
                elif var == 'N':
                    res = rq.post('http://127.0.0.1:8000/storage/deletefile/', data={'name':sys.argv[1],'password':sys.argv[2],'filename':item})
                    print('Deleting ',item)
                else:
                    item="\""+item+"\""
                    if sc=='1':
                        os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                    elif sc=='2': 
                        os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6])
                    elif sc=='3':
                        os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                    print('Downloading exclusive ',item)
        else:
            with open(item,'rb') as rf:
                cont = rf.read()
                conte = cont.decode('ISO-8859-1')
                #print('decrypting')
                if sc=='status':
                    if sys.argv[5]=='1':
                        key=sys.argv[6]
                        arc=ARC4.new(key)
                        cont=arc.encrypt(cont)

                    if sys.argv[5]=='2':
                        key=sys.argv[6]
                        iv=sys.argv[7]
                        aes=AES.new(key,AES.MODE_CBC,iv)
                        extra=len(conte)%16
                        if extra>0:
                            conte=conte+(' '*(16-extra))
                        conte = conte.encode('ISO-8859-1') 
                        cont=aes.encrypt(conte)
         
                    if sys.argv[5]=='3':
                        key=sys.argv[6]
                        key=key.encode('utf-8')
                        d=blowfish.Cipher(key) 
                        extra=len(conte)%8
                        if extra>0:
                            conte=conte+(' '*(8-extra))
                        conte = conte.encode('ISO-8859-1') 
                        cont=b"".join(d.encrypt_ecb(conte))

                else:
                    if sc=='1':
                        key=sys.argv[5]
                        arc=ARC4.new(key)
                        cont=arc.encrypt(cont)

                    if sc=='2':
                        key=sys.argv[5]
                        iv=sys.argv[6]
                        aes=AES.new(key,AES.MODE_CBC,iv)
                        extra=len(conte)%16
                        if extra>0:
                            conte=conte+(' '*(16-extra))
                        conte = conte.encode('ISO-8859-1') 
                        cont=aes.encrypt(conte)
         
                    if sc=='3':
                        key=sys.argv[5]
                        key=key.encode('utf-8')
                        d=blowfish.Cipher(key) 
                        extra=len(conte)%8
                        if extra>0:
                            conte=conte+(' '*(8-extra))
                        conte = conte.encode('ISO-8859-1') 
                        cont=b"".join(d.encrypt_ecb(conte))

                md5 = hashlib.md5(cont).hexdigest()
                
                #print(md5)  
                #print(jsond[item])
                #print(jsond[item]) 

                if not md5 == jsond[item[len(bstrt):]]:
                    #print(item)
                    if sc=='status':
                        cs=cs+item[len(bstrt):]+'\n'
                    else:
                        timeout = 30
                        t = threading.Timer(timeout, helper)
                        t.start()
                        prompt = "Files exist locally and at server. '1' for server copy, '2' for local copy "+item+"\n"
                        var = input(prompt) 
                        t.cancel() 

                #print('UU')
                        if var is None:
                            res = rq.post('http://127.0.0.1:8000/storage/lockfree/', data={'name':sys.argv[1],'password':sys.argv[2]})
                        elif var == '1':
                            item="\""+item+"\""
                            if sc=='1':
                                os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                            elif sc=='2':
                                os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6])
                            elif sc=='3':
                                os.system('python3 download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                            print('Downloading overwrite ',item)
                        else: 
                            item="\""+item+"\""
                            if sc=='1':
                                os.system('python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                            elif sc=='2':
                                os.system('python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6])
                            elif sc=='3':
                                os.system('python3 upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item+' '+sys.argv[4]+' '+sys.argv[5])
                            print('Uploading overwrite ',item)

                else:
                    csm=csm+item[len(bstrt):]+'\n'

    if sc=='status':
        finalS=''
        if ce!='':
            finalS = finalS+'Files exclusively on client\n'
            finalS = finalS+ce+'\n'
            print('Files exclusively on client')
            print(ce)
        if se!='':
            finalS = finalS+'Files exclusively on server\n'
            finalS = finalS+se+'\n'
            print('Files exclusively on server')
            print(se)
        if csm!='':
            finalS = finalS+'Files both on client and server, contents match\n'
            finalS = finalS+csm+'\n'
            print('Files both on client and server, contents match')
            print(csm)
        if cs!='':
            finalS = finalS+'Files both on client and server, contents different\n'
            finalS = finalS+cs+'\n'
            print('Files both on client and server, contents different')
            print(cs)
        with open('/tmp/temp.txt', 'w') as wf:
            wf.write(finalS)

    else: 
        r = rq.post('http://127.0.0.1:8000/storage/end/', data={'name':sys.argv[1], 'password':sys.argv[2]})
        '''rld = json.loads(r.content.decode())
        if rld['syncing'] == 'failed':
            print('Sync Failed')
        if rld['syncing'] == 'done':
            print('Sync Successful')'''
