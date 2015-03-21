from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import search, attachment

urlpatterns = patterns('',
    # Empty query.
    url(r'^\s+/.*$', RedirectView.as_view(url='/@/')),

    # Redirect to one with a slash.
  # url(r'^[^/]+$', RedirectView.as_view(url='')),

    # The actual message/thread
    url(r'^([^/]+)/$', search),
    url(r'^([^/]+)/([0-9]+)$', attachment),
)
