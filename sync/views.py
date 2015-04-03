from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout

from social.backends.utils import load_backends
from social.apps.django_app.utils import psa

from sync.models import Sync, Account, Folder
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

import kloudless; kloudless.configure(api_key=settings.KLOUDLESS_API_KEY)

def index(request):
    data = {}
    if request.user.is_authenticated():
        user_syncs = Sync.objects.filter(user=request.user)
        data['user_syncs'] = user_syncs
        data['kloudless_app_id'] = settings.KLOUDLESS_APP_ID
        return render(request, 'sync/dashboard.html', data)
    else:
    	return render(request, 'sync/login.html', data)

def logout(request):
    django_logout(request)
    return redirect('sync:index')

def login(request):
    data = {}
    return render(request, 'sync/login.html', data)

def new_sync(request):
    origin_account_id = request.POST.get('origin_account_id')
    origin_id = request.POST.get('origin_id')
    origin_name = request.POST.get('origin_name')
    origin_path = request.POST.get('origin_path')
    
    dest_account_id = request.POST.get('dest_account_id')
    dest_id = request.POST.get('dest_id')
    dest_name = request.POST.get('dest_name')
    dest_path = request.POST.get('dest_path')
    
    if not origin_account_id:
        messages.error("No origin account specified.") 
        return redirect('sync:index')
    if not origin_path:
        origin_path = 'EMPTY' #STUPID FIX FOR NOW
    
    if not dest_account_id:
        messages.error("No destination account specified.") #
        return redirect('sync:index')
    if not dest_path:
        dest_path = 'EMPTY' #STUPID FIX FOR NOW
    
    sync_account = Sync()
    sync_account.user = request.user
    
    try:
        origin = Folder.objects.get(kloudless_id=origin_id)
    except ObjectDoesNotExist:
        origin = Folder()
        origin.kloudless_id = origin_id
        origin.name = origin_name
        origin.path = origin_path

    try:
        origin_account = Account.objects.get(kloudless_id=origin_account_id)
        origin.account = origin_account
    except ObjectDoesNotExist:  
        kloud_account = kloudless.Account.retrieve(id=origin_account_id)
        #Add error for retrieivng Kloudless account`
        origin_account = Account()
        origin_account.kloudless_id = origin_account_id
        origin_account.name = kloud_account.account
        origin_account.root = origin
        origin_account.service = kloud_account.service_name
        origin_account.full_clean()
        origin_account.save()
        origin.account = origin_account 
    
    origin.full_clean()
    origin.save()
    sync_account.origin_root = origin
    sync_account.origin_account = origin_account
    
    try:
        dest = Folder.objects.get(kloudless_id=dest_id)
    except ObjectDoesNotExist:
        dest = Folder()
        dest.kloudless_id = dest_id
        dest.name = dest_name
        dest.path = dest_path
   
    try:
        dest_account = Account.objects.get(kloudless_id=dest_account_id)
        dest.account = dest_account
    except ObjectDoesNotExist: 
        kloud_account = kloudless.Account.retrieve(id=dest_account_id)
        # add excpetion for kloudless
        dest_account = Account()
        dest_account.kloudless_id = dest_account_id
        dest_account.name = kloud_account.account
        dest_account.root = dest
        dest_account.service = kloud_account.service_name
        dest_account.full_clean()
        dest_account.save()
        dest.account = dest_account
   
    dest.full_clean()
    dest.save()
    sync_account.dest_root = dest
    sync_account.dest_account = dest_account
    sync_account.full_clean()
    sync_account.save()
    #return render(request, 'sync/dashboard.html', data)
    return index(request)
