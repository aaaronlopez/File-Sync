from django.db import models
from django.contrib.auth.models import User

class Sync(models.Model):
    user = models.ForeignKey(User) 
    origin_account = models.ForeignKey('Account', related_name='o_account_sync')
    origin_root = models.ForeignKey('Folder', related_name='o_root_sync')
    dest_account = models.ForeignKey('Account', related_name='d_account_sync') 
    dest_root = models.ForeignKey('Folder', related_name='d_root_sync')

class Account(models.Model):
    kloudless_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    cursor = models.CharField(max_length=200, default='after-auth')
    service = models.CharField(max_length=20)

class Folder(models.Model):
    kloudless_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, blank=True, default='') 
    account = models.ForeignKey('Account', related_name='folder') 
    parent = models.ForeignKey('Folder', blank=True)

class File(models.Model):
    kloudless_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, blank=True, default='') 
    account = models.ForeignKey('Account', related_name='file') 
    parent = models.ForeignKey('Folder')
