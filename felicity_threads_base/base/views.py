from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse

def index(request):
    messages.add_message(request , messages.INFO , "Hello World")
    return HttpResponse("There are some things better left unseen.")
