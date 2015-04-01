from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from .views import index, docs

urlpatterns = patterns('',
    url(r'^/?$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/?$', docs),
    url(r'^popular/?$', TemplateView.as_view(template_name = 'popular.html')),

    url(r'^\+$', RedirectView.as_view(url='/+/')),
    url(r'^\+/$', 'search.views.search'),
    url(r'^schedule/', include('schedule.urls')),

    url(r'^@/', include('mail.urls')),

    url(r'^!/', include('articles.urls')),
    url(r'^source/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ARTICLES_DIR, 'show_indexes': True}),

    url(r'^track$', 'tracking.views.track_xhr'),
)
