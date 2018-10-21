import requests as rq
import json
import hashlib
import sys
import os
import subprocess

res = rq.post('http://127.0.0.1:8000/storage/md5s', data={'name':sys.argv[1], 'password':sys.argv[2]})

jsond = json.loads(res.content.decode())
comm = 'find '+sys.argv[3]+' -type f'
files = subprocess.check_output(comm, shell=True).decode().split('\n')
for item in files:
    if item not in jsond.keys():
        os.system('python upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item)
for item in jsond.keys():
    if item not in files:
        var = input('File exists in server. Want to download?')
        if var == 'N':
            os.system('python delete_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item)
        else:
            os.system('python download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item)
    else:
        with open(item,'rb') as rf:
            cont = rf.read()
            conte = cont.decode('ISO-8859-1')
            md5 = hashlib.md5(conte).hexdigest()
            if not md5 == jsond[item]:
                var = input('Files exist locally and at server. '1' for server copy, '2' for local copy')
                if var == '1':
                    os.system('python download_client1.py '+sys.argv[1]+' '+sys.argv[2]+' '+item)
                else:
                    os.system('python upload_client.py '+sys.argv[1]+' '+sys.argv[2]+' '+item)
