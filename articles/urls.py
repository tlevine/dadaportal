import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponsePermanentRedirect

from .views import article, index

urlpatterns = patterns('',
    url(r'^$', index, name = 'articles/index'),
    url(r'^(.+)/$', article, name = 'articles/article'),
    url(r'^([^/]+)$', lambda _, x: HttpResponsePermanentRedirect('/!/%s/' % x)),

    # Only for development
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ARTICLES_DIR}),
)
