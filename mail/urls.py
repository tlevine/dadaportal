from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import index, message, message_legacy, attachment

# Allow for queries to contain slashes
urlpatterns = patterns('',
    url(r'^$', index, name = 'mail/index'),
    url(r'^(.+)/$', message, name = 'mail/message'),
    url(r'^id:(.+)/$', message_legacy, name = 'mail/message_legacy'),
    url(r'^(.+)/([0-9]+)$', attachment, name = 'mail/attachment'),
)
