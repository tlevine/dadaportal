import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

from .views import article, IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name = 'articles/index'),
    url(r'^(.+)/$', article, name = 'articles/article'),
    url(r'^([^/]+)$', lambda _, x: HttpResponseRedirect('/!/%s/' % x)),

    # Only for development
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ARTICLES_DIR}),
)
