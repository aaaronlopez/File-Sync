from __future__ import absolute_import

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings

from celery import shared_task
from sync.models import Sync, Account, Folder, File

import logging
logger = logging.getLogger(__name__) #check logger config in settings.py

import kloudless; kloudless.configure(api_key=settings.KLOUDLESS_API_KEY)

@shared_task(ignore_result=True)
def process(account_id):
    #To DO: add try statements where appropriate
    #handle the case when there are more than 1 syncs with this account
    import pdb; pdb.set_trace()
    try:
        account = Account.objects.get(kloudless_id=account_id)
    except ObjectDoesNotExist:
        logger.error("No such account with the provided account_id exists.") 
        return
        # not sure if this should be something other than error
    try:
        sync = Sync.objects.get(origin_account=account)
    except ObjectDoesNotExist:
        logger.error("No such sync account with the provided origin account exists.") 
        return
        # same for here:  not sure if this should be something other than error
    k_origin_account = kloudless.Account.retrieve(account.kloudless_id)
    k_origin_folder = kloudless.Folder.retrieve(id=sync.origin_root.kloudless_id,
                                                    parent_resource=k_origin_account)
   
    dest_account = sync.dest_account
    k_dest_account = kloudless.Account.retrieve(dest_account.kloudless_id)
    k_dest_folder = kloudless.Folder.retrieve(id=sync.dest_root.kloudless_id, 
                                                parent_resource=k_dest_account)
    
    events = k_origin_account.events.all(cursor=account.cursor)
    current_event = events[1]
    metadata = current_event.metadata
    
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
           
            k_origin_file = kloudless.Files.retrieve(id=current_event.id, 
                                                    parent_resource=k_origin_account)#check this
            k_dest_file = k_origin_file.copy_file(parent_id=k_dest_folder.id, 
                                                    account=k_dest_account.id)

            dest_file = File()
            dest_file.kloudless_id = k_dest_file.id
            dest_file.name = k_dest_file.name
            dest_file.path = k_dest_file.path
            dest_file.account = dest_account
            dest_file.parent = sync.dest_root #fix this
            dest_file.full_clean()
            dest_file.save()

        #ADD SYNCING FOLDERS LATER
        #if metadata.type == 'folder':
        #    origin_folder = Folder 
    
    if current_event.type == 'update':
        if metadata.type == 'file':
            k_origin_file = kloudless.File.retrieve(id=current_event.id, 
                                                    parent_resource=k_origin_account)#check this
            k_dest_file = k_origin_file.copy_file(parent_id=k_dest_folder.id,
                                                    account=k_dest_account.id)


        #ADD SYNCING FOLDERS LATER    

#MAKE EACH DIFFERENT EVENT INTO DIFFERENT FUNCTIONS
        

    account.cursor = events.cursor
    account.full_clean()
    account.save()
    
    #fix what you return
    return 1

