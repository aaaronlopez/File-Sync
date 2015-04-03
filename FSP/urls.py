from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from sync import views

urlpatterns = patterns('',
    url(r'^fsp-admin/', include(admin.site.urls)),
    url(r'', include('sync.urls', namespace="sync")),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
