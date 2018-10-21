from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.contrib.auth import authenticate, login
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3

def upload(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        if
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
            pass
        usrfl.save()
        #usrfl.owners.add(session.query(models.MyUser).filter_by(username=request.user.username).first())
        html = "<html><body>Success bro</body></html>"
        return HttpResponse(html)
    else:
        html = "<html><body>You must be logged in to perform following activity.</body></html>"
        return HttpResponse(html)

def download(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        for temp in usrt.files.all():
            flname = temp.filename[len(uname):]
            data[flname] = temp.content.decode('utf-8')
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        html = "<html><body>You must be logged in to perform following activity.</body></html>"
        return HttpResponse(html)
