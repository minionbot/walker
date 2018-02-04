from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from octopus.main.models import *

def index(request):
    return HttpResponse("Hello, My Stamps count is %s" % len(Cover.objects.all()))
