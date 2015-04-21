from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

from .views import index, docs

def fix_dir(old, new):
    return url(r'^%s(/(?:.+)?)$' % old,
               lambda _, x: HttpResponsePermanentRedirect('/%s%s' % (new, x)))

def fix_tag(tag):
    return url(r'^%s/?$' % tag, RedirectView.as_view(url='/!/?tag=%s' % tag))

urlpatterns = patterns('',
    url(r'^/?$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/$', docs),
    url(r'^popular/$', TemplateView.as_view(template_name = 'popular.html')),

    url(r'^\+/$', 'search.views.search'),
#   url(r'^schedule/', include('schedule.urls')),

    url(r'^@/', include('mail.urls')),

    url(r'^!/', include('articles.urls')),
    url(r'^source/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ARTICLES_DIR, 'show_indexes': True}),

    url(r'^track/', include('tracking.urls')),

    url(r'^jobs/$', 'job.views.job'),

    # Backwards compatibility
    fix_tag('open-data'),
    fix_tag('socrata'),
    fix_tag('convert'),
    fix_tag('sensing-data'),
    fix_tag('learn'),
    fix_tag('shenanigans'),
    fix_tag('letterpress'),

    fix_dir('notes', '!/notes'),
    fix_dir('__33__', '!'),
    fix_dir('dada', '!'),
    fix_dir('scarsdale', '!/scarsdale'),
    fix_dir('stuff', '!/stuff'),
   #fix_dir('schedule', ''),

    # Slashes
    url(r'^(.+[^/])$', lambda _, x: HttpResponseRedirect('/%s/' % x)),
)
