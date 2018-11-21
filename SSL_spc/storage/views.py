from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.contrib.auth import authenticate, login
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import hashlib
import urllib
from urllib.parse import quote

def upload(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        if hashlib.md5(request.POST['content'].encode('ISO-8859-1')).hexdigest() != request.POST['md5']:
            return HttpResponse(json.dumps({'checksum':'false'}))
        try:
            usrfl = models.userFile.objects.get(filename=user.username+request.POST['filename'])
        except models.userFile.DoesNotExist:
            usrfl = models.userFile()
        usrfl.filename = user.username+request.POST['filename']
        usrfl.content = bytes(request.POST['content'], encoding='utf-8')
        usrfl.save()
        try:
            temp = models.MyUser.objects.get(username=user.username)
            temp.files.add(usrfl)
            temp.save()
        except models.MyUser.DoesNotExist:
            return HttpResponse(json.dumps({'checksum':'true'}))
        usrfl.save()
        #usrfl.owners.add(session.query(models.MyUser).filter_by(username=request.user.username).first())
        return HttpResponse(json.dumps({'checksum':'true'}))
    else:
        return HttpResponse(json.dumps({'checksum':'true'}))

def download(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        for temp in usrt.files.all():
            flname = temp.filename[len(uname):]
            data[flname] = [temp.content.decode('utf-8'),hashlib.md5(temp.content.decode('utf-8')).hexdigest()]
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        html = "<html><body>You must be logged in to perform following activity.</body></html>"
        return HttpResponse(html)

def download1(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        try:
            temp =  usrt.files.get(filename=uname+request.POST['filename'])
            flname = temp.filename[len(uname):]
            data[flname] = [temp.content.decode('utf-8'),hashlib.md5(temp.content.decode('utf-8').encode('ISO-8859-1')).hexdigest()]
        except models.userFile.DoesNotExist:
            return HttpResponse(json.dumps({'userFail':'true'}))
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        return HttpResponse(json.dumps({'userFail':'true'}))

def md5s(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        for temp in usrt.files.all():
            flname = temp.filename[len(uname):]
            data[flname] = hashlib.md5(temp.content.decode('utf-8').encode('ISO-8859-1')).hexdigest()
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        return HttpResponse(json.dumps({'userFail':'true'}))

def deletefile(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        try:
            temp =  usrt.files.get(filename=uname+request.POST['filename'])
            temp.delete()
        except models.userFile.DoesNotExist:
            return HttpResponse(json.dumps({'userFail':'true'}))
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        return HttpResponse(json.dumps({'userFail':'true'}))

def direct_Str(request):
    if request.user.is_authenticated:
        uname = request.user.username
        usrt = models.MyUser.objects.get(username=uname)
        iflnames = [];flnames = [];
        for temp in usrt.files.all():
            iflnames.append(temp.filename)
        strt = request.GET.get('directn', uname)
        print(strt)
        for temp in iflnames:
            if temp.find(strt) == 0:
                flnames.append(temp)
        print(flnames)
        html = "<p>This is the current list of files</p> <ul> Files"
        vfls = []
        for temp in flnames:
            tempst = temp[len(strt)+1:]
            num = tempst.find('/')
            if num == -1:
                htst = '''<li><a href="http://127.0.0.1:8000/storage/openFile/?filename='''+temp+'''">'''+tempst+"</a></li>"
                tempht = html+htst
                html = tempht
            else:
                tempst2 = tempst[:num]
                if tempst2 not in vfls:
                    htst = '''<li><a href="http://127.0.0.1:8000/storage/direct_Str/?directn='''+urllib.parse.quote(strt+'/'+tempst2, safe='')+'''">'''+tempst2+"</a></li>"
                    tempht = html+htst
                    html = tempht
                    vfls.append(tempst2)
                else:
                    pass
            tempht = html + "</ul>"
            html = tempht
    else:
        html = "<p>You need to login to perform this operation</p>"
    return HttpResponse(html)
