from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages as notifications

from myWebSite.messagingSystem.forms import SignUpForm, MessageForm
from myWebSite.messagingSystem.models import Message
from django.contrib.auth.models import User


import mimetypes
from django.http import HttpResponse

import sqlite3 as sql
import os
import csv
from sqlite3 import Error

from django.core.management import call_command
from myWebSite.encryption import *


def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            notifications.success(request,'Registration Done!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def inbox(request):
    text_messages = Message.objects.filter(receiver=request.user).order_by('-time')
    i=0
    while(i<len(text_messages)):
        text_messages[i].content = decrypt(text_messages[i].content)
        i+=1
    context = {
         'text_messages': text_messages
      }
    return render(request, 'inbox.html', context)

@login_required
def outbox(request):
    out_text_messages = Message.objects.filter(sender=request.user).order_by('-time')
    i=0
    while(i<len(out_text_messages)):
        out_text_messages[i].content = decrypt(out_text_messages[i].content)
        i+=1
    context = {
         'out_text_messages': out_text_messages
      }
    return render(request, 'outbox.html', context)

@login_required
def send(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                sender=request.user,
                receiver=User.objects.get(username=form.cleaned_data["receiver"]),
                content=encrypt(form.cleaned_data["content"]),
             )
            message.save()
            notifications.success(request,'Message Sent Successfully at {}'.format(message.time))
            #return redirect('home')
            form = MessageForm()

    else:
        form = MessageForm()
    return render(request, 'send.html', {'form': form})

def download(request):

    fl_path = os.getcwd() + "/dbdump.json"
    filename = 'dbdump.json'

    output = open(filename,'w')
    # call_command('dumpdata','messagingSystem.Message',format='json',indent=3,stdout=output)
    call_command('dumpdata',format='json',indent=3,stdout=output)
    # call_command('dumpdata','auth.user',format='json',indent=3,stdout=output)
    output.close()

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def dbdump(request):
    return render(request, 'dbdump.html')
