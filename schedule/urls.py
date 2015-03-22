from django.conf.urls import patterns, url

from .views import day, month

urlpatterns = patterns('',
    url(r'^$', day),
    url(r'month/?$', month),
)
