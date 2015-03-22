from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import index

urlpatterns = patterns('',
    url(r'^/?$', index),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^\+$', RedirectView.as_view(url='/+/')),
    url(r'^\+/$', 'search.views.search'),

    url(r'^schedule/?$', 'schedule.views.schedule'),

    url(r'^@/', include('mail.urls')),

    url(r'^!/', include('articles.urls')),
    url(r'^source/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ARTICLES_DIR, 'show_indexes': True}),

    url(r'^track$', 'tracking.views.track_xhr'),
)
