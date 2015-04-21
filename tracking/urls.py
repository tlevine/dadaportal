from django.conf.urls import patterns, include, url

from .views import overview, followup_ico, followup_js

urlpatterns = patterns('',
    url(r'^$', overview),
    url(r'^followup\.ico$', followup_ico, name = 'followup-img'),
    url(r'^followup\.js$', followup_js, name = 'followup-xhr'),
)
