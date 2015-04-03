from django.db import models
from django.contrib.auth.models import User

class Sync(models.Model):
    user = models.ForeignKey(User) 
    origin_account = models.ForeignKey('Account', related_name='origin_account')
    origin_root = models.ForeignKey('Folder', related_name='origin_root')
    dest_account = models.ForeignKey('Account', related_name='dest_account') 
    dest_root = models.ForeignKey('Folder', related_name='dest_root')

class Account(models.Model):
    kloudless_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    cursor = models.CharField(max_length=200, default='0')
    service = models.CharField(max_length=20)

class Folder(models.Model):
    kloudless_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, default='EMPTY') 
    account = models.ForeignKey('Account', related_name='folder_account') #Check NULL and BLANK
    # parent = models.ForeignKey('Folder', null=True)

class File(models.Model):
    kloudless_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, default='EMPTY') #check this
    account = models.ForeignKey('Account', related_name='file_account') #Check NULL and BLANK
    # parent = models.ForeignKey('Folder')
