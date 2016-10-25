# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('hyperkitty.views.index.index'),
        permanent=True)),
    url(r'^admin/', include('postorius.urls')),
    url(r'^archives/', include('hyperkitty.urls')),
    url(r'', include('django_mailman3.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^django-admin/', include(admin.site.urls)),
]
