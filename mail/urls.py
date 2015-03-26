from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import search, attachment

urlpatterns = patterns('',
    # Empty query.
    url(r'^\s+/.*$', RedirectView.as_view(url='/@/')),
    url(r'^$', RedirectView.as_view(url='/+/')),

    # The actual message/thread
    # Allow for queries to contain slashes
    url(r'^(.+)/([0-9]+)$', attachment),
    url(r'^(.+)/$', search),
)
