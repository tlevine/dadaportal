from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import message, message_legacy, attachment

urlpatterns = patterns('',
    # Empty query.
    url(r'^\s+/.*$', RedirectView.as_view(url='/@/')),
    url(r'^$', RedirectView.as_view(url='/+/')),

    # The actual message/thread
    # Allow for queries to contain slashes
    url(r'^(.+)/$', message, name = 'mail/message'),
    url(r'^id:(.+)/$', message_legacy, name = 'mail/message_legacy'),
    url(r'^(.+)/([0-9]+)$', attachment, name = 'mail/attachment'),
)
