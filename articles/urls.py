from django.conf.urls import patterns, include, url

from .views import article_dynamic

urlpatterns = patterns('',
    url(r'^([^/]+)/$', article_dynamic),

    # Something other than 404?
   #url(r'^$',

    # Static
   #url(r'.+$', 
)
