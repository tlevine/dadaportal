from django.conf import settings
from django.conf.urls import patterns, include, url

from .views import article

urlpatterns = patterns('',
    url(r'^(.+)/$', article),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ARTICLES_DIR}),

    # Something other than 404?
   #url(r'^$',

    # Static
   #url(r'.+$', 
)
