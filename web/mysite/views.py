from django.shortcuts import render
from django.http import HttpResponse
import time
# Create your views here.

def index(request):
    time.sleep(3)
    return HttpResponse("Test")
