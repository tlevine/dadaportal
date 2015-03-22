from django.conf.urls import patterns, url

from .views import index, day, month

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'day/?$', day),
    url(r'month/?$', month),
)
