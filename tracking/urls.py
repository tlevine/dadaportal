from django.conf.urls import patterns, include, url

from .views import analyze, followup_png, followup_js

urlpatterns = patterns('',
    url(r'^$', analyze),
    url(r'^followup\.png$', followup_png),
    url(r'^followup\.js$', followup_js),
)
