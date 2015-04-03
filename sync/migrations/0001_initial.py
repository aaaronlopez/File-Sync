# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('kloudless_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('cursor', models.CharField(default=b'0', max_length=200)),
                ('service', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('kloudless_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('path', models.CharField(default=b'EMPTY', max_length=200)),
                ('account', models.ForeignKey(related_name='file_account', to='sync.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('kloudless_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('path', models.CharField(default=b'EMPTY', max_length=200)),
                ('account', models.ForeignKey(related_name='folder_account', to='sync.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sync',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dest_account', models.ForeignKey(related_name='dest_account', to='sync.Account')),
                ('dest_root', models.ForeignKey(related_name='dest_root', to='sync.Folder')),
                ('origin_account', models.ForeignKey(related_name='origin_account', to='sync.Account')),
                ('origin_root', models.ForeignKey(related_name='origin_root', to='sync.Folder')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
