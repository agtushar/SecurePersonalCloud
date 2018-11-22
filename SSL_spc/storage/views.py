from django.shortcuts import render
from django.http import HttpResponse
import mimetypes
from .forms import PostForm
import requests
from django.shortcuts import redirect
import base64
from django.template import loader
from django.contrib.auth import authenticate, login
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import hashlib
import pyDes
from pyDes import des
import urllib
from urllib.parse import quote
from .forms import PostForm

def upload(request):
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        if hashlib.md5(request.POST['content'].encode('ISO-8859-1')).hexdigest() != request.POST['md5']:
            return HttpResponse(json.dumps({'checksum':'false'}))
        try:
            usrfl = models.userFile.objects.get(filename=user.username+'/'+request.POST['filename'])
        except models.userFile.DoesNotExist:
            usrfl = models.userFile()
        usrfl.filename = user.username+'/'+request.POST['filename']
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
    """returns file names and their md5 hashes"""
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        for temp in usrt.files.all():
            flname = temp.filename[len(uname)+1:]
            data[flname] = [temp.content.decode('utf-8'),hashlib.md5(temp.content.decode('utf-8')).hexdigest()]
        resp = HttpResponse(json.dumps(data))
        return resp
    else:
        html = "<html><body>You must be logged in to perform following activity.</body></html>"
        return HttpResponse(html)

def download1(request):
    """returns filename and data"""
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        uname = request.POST['name']
        usrt = models.MyUser.objects.get(username=uname)
        data = {}
        try:
            temp =  usrt.files.get(filename=uname+'/'+request.POST['filename'])
            flname = temp.filename[len(uname)+1:]
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
            flname = temp.filename[len(uname)+1:]
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
            temp =  usrt.files.get(filename=uname+'/'+request.POST['filename'])
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
        strt = request.GET.get('directn', uname+'/')
        print(strt)
        for temp in iflnames:
            if temp.find(strt) == 0:
                flnames.append(temp)
        print(flnames)
        html = "<p>This is the current list of files</p> <ul> Files"
        vfls = []
        for temp in flnames:
            tempst = temp[len(strt):]
            num = tempst.find('/')
            if num == -1:
                htst = '''<li><a href="http://127.0.0.1:8000/storage/keyVerify/?filename='''+temp+'''">'''+tempst+"</a></li>"
                tempht = html+htst
                html = tempht
            else:
                tempst2 = tempst[:num]
                if tempst2 not in vfls:
                    htst = '''<li><a href="http://127.0.0.1:8000/storage/direct_Str/?directn='''+urllib.parse.quote(strt+tempst2+'/', safe='')+'''">'''+tempst2+"</a></li>"
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

def keyVerify(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            uname = request.user.username
            flname = request.GET.get('filename')
            form = PostForm(request.POST)
            key1 = form.cleaned_data.get('key1')
            key2 = form.cleaned_data.get('key2')
            schema = form.cleaned_data.get('schema')
            return redirect('displayFile',flname)
        else:
            print("herobro")
            form = PostForm()
            return render(request, 'cipher.html', {'form': form})

def display(request,filen):
    user = None
    html=""
    if request.user.is_authenticated:
        user = request.user.username
    else:
        html = "<html><body>You must be logged in to perform following activity.</body></html>"
        return HttpResponse(html)
    if user is not None:
        uname = user
        usrt = models.MyUser.objects.get(username=uname)
        temp = usrt.files.get(filename=filen)
        data = {}
        context={}
        flname = temp.filename[len(uname):]
        data[flname] = temp.content.decode('utf-8').encode('ISO-8859-1')
        # decyrpt data here
        key="011bytes"
        key = key.encode('utf-8')
        d = des(key)
        decrypteddata =d.decrypt(data[flname])
        y = decrypteddata.decode('ISO-8859-1')
        c = y.rstrip()
        context["filename"] = flname
        type=mimetypes.guess_type(flname)[0]
        type=type[:type.find("/")]
        if (type=="image"):
            c = base64.b64encode(c.encode('ISO-8859-1'))
            context["image"] = c.decode()
            template=loader.get_template('web_client/image.html')
        elif (type=="video"):
            c = base64.b64encode(c.encode('ISO-8859-1'))
            context["video"] = c.decode()

            template=loader.get_template('web_client/video.html')
        elif (type=="text"):
            plaindat=c.encode('ISO-8859-1')
            b64bin = base64.b64encode(c.encode('ISO-8859-1'))
            context["text"] = plaindat.decode()
            context["b64"]=b64bin.decode()

            template=loader.get_template('web_client/rendertext.html')

        # response = HttpResponse(content_type=mimetypes.guess_type(flname))
        # response['Content-Disposition'] = 'attachment; filename=%s' % flname  # force browser to download file
        # response.write(data[flname])
        # return response

        return HttpResponse(template.render(context,request))