from django.conf.urls import patterns, include, url

from .views import article

urlpatterns = patterns('',
    url(r'^[^/]+/$', article),

    # Something other than 404?
   #url(r'^$',

    # Static
   #url(r'.+$', 
)
