from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from .models import LoginUser
from controller.social import *
import os
import threading
from controller.portscan import port_infor
from controller.sub import sub
from controller.allc import ScanC
# Create your views here.



class MyForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"js@dashboard.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"******"}))

class SocialPass(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={"id":"keyword","class":"form-control"}))


def index(request):
    try:
        if request.GET['logout']:
            del request.session["username"]
    except KeyError:
        pass
    try:
        if request.session.get("username") is None:
            return HttpResponseRedirect("/login")
    except:
        return HttpResponseRedirect("/login")

    passList = []

    cores = get_core()
    if request.POST:
        text = SocialPass(request.POST)
        if text.is_valid():
            keyword = text.cleaned_data['keyword']
            passList = get_query(keyword,cores)
    else:
        text = SocialPass()

    context={"username":request.session.get("username"),"is_admin":True,"form":text,"cores":cores,"keyword":passList}
    return render(request,"index.html",context=context)


class formSubdomain(forms.Form):
    domain = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

def domain(request,var):
    res,message = port_infor(var)
    for i in res:
        res[i] = eval(res[i])
    print res
    return render(request,"domain.html",context={"ip":var,"res":res,"message":message})

def subdomain(request):
    domain = ""
    message = ""
    result = {}
    if request.method == "POST":
        form = formSubdomain(request.POST)
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            result,message = sub(domain)
    else:
        form = formSubdomain()
    return render(request,"subdomain.html",context={"request":request,"MyForm":form,"input":domain,"res":result,"Msg":message})

def allC(request,ip):
    result,message = ScanC(ip)
    return render(request,"allC.html",context={"requests":request,"ip":ip,"result":result,"message":message})

def weakhunt(request):
    return render_to_response("weakhunt.html",context={"request":request})

def login(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = LoginUser.objects.filter(name__exact = username)
        if user.filter(password = password).exists():
            request.session['username'] = user[0].name
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/login")

    else:
        form = MyForm()
        return render(request,"login.html",context={'form':form})