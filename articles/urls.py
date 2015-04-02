from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponsePermanentRedirect

from .views import article_cached, article_canonical, index

article = article_cached if settings.IS_PRODUCTION else article_canonical

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^(.+)/$', article),
    url(r'^([^/]+)$', lambda _, x: HttpResponsePermanentRedirect('/!/%s/' % x)),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ARTICLES_DIR}),

    # Something other than 404?
   #url(r'^$',
)
