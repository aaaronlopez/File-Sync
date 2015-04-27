from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^newsync/$', views.new_sync, name='new-sync'),
    url(r'^syncprocess/$', views.sync_process, name='sync-process'),
)
