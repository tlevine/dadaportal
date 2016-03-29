from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import IndexView, message, message_legacy, attachment

# Allow for queries to contain slashes
urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name = 'mail/index'),
    url(r'^id:(.+)/$', message_legacy, name = 'mail/message_legacy'),
    url(r'^(.+)/$', message, name = 'mail/message'),
    url(r'^(.+)/([0-9]+)$', attachment, name = 'mail/attachment'),
)
