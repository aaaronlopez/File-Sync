from __future__ import absolute_import

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings

from celery import shared_task
from sync.models import Sync, Account, Folder, File

import kloudless; kloudless.configure(api_key=settings.KLOUDLESS_API_KEY)

@shared_task
def process(account_id):
    try:
        account = Account.objects.get(kloudless_id=account_id)
    except ObjectDoesNotExist:
        messages.error("No such account with the provided account_id exists.") 
        #fix this
    try:
        sync = Sync.objects.get(origin_account=account)
    except ObjectDoesNotExist:
        messages.error("No such sync account with the provided account exists.") 
        #fix this
    k_origin_account = kloudless.Account.retrieve(account.kloudless_id)
    events = k_origin_account.events.all(account.cursor)
    current_event = events[1]
    metadata = current_event.metadata

    dest_account = sync.dest_account
    k_dest_account = kloudless.Account.retrieve(destination.kloudless_id)
    k_origin_folder = kloudless.Folders.retrieve(id=sync.origin_root.kloudless_id)
    k_dest_folder = kloudless.Folders.retrieve(id=sync.dest_root.kloudless_id)
    
    if current_event.type == 'add':
        if metadata.type == 'file':
            origin_file = File()
            origin_file.kloudless_id = current_event.id
            origin_file.name = metadata.name
            origin_file.path = metadata.path
            origin_file.account = account
            origin_file.parent = sync.origin_root #fix this
            origin_file.full_clean()
            origin_file.save()
           
            k_origin_file = kloudless.Files.retrieve(name=current_event.name)#check this
            
            #saving on kloudless
            #To DO: add try statements where appropriate
            
            #USE COPY ENDPOINT:T
            k_dest_file = k_origin_file.copy_file(parent_id=k_dest_folder.id, account=k_dest_account.id)

            dest_file = File()
            dest_file.kloudless_id = k_dest_file.id
            dest_file.name = k_dest_file.name
            dest_file.path = k_dest_file.path
            dest_file.account = k_dest_file.account
            dest_file.parent = sync.origin_root #fix this
            dest_file.full_clean()
            dest_file.save()
        
        #ADD SYNCING FOLDERS LATER
        #if metadata.type == 'folder':
        #    origin_folder = Folder 


#MAKE EACH DIFFERENT EVENT INTO DIFFERENT FUNCTIONS
        

    account.cursor = events.cursor
    account.full_clean()
    account.save()

