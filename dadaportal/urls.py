from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

from .views import docs, infinite_redirect

def fix_dir(old, new):
    return url(r'^%s(/(?:.+)?)$' % old,
               lambda _, x: HttpResponsePermanentRedirect('/%s%s' % (new, x)))

def fix_tag(tag):
    return url(r'^%s/?$' % tag, RedirectView.as_view(url='/!/?tag=%s' % tag))

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name = 'dadaportal/index.html'),
        name = 'dadaportal/index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/$', docs),
    url(r'^recommended/$',
        TemplateView.as_view(template_name = 'dadaportal/recommended.html'),
        name = 'dadaportal/recommended'),


    url(r'^search/', include('haystack.urls')),
#   url(r'^schedule/', include('schedule.urls')),

    url(r'^@/', include('mail.urls')),

    url(r'^!/', include('articles.urls')),
    url(r'^source/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ARTICLES_DIR, 'show_indexes': True}),

    url(r'^track/', include('tracking.urls')),

    url(r'^jobs/$', 'jobs.views.jobs', name = 'jobs'),

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

    url(r'^img/pink_hat_icon-200.png/?$',
        RedirectView.as_view(url='/static/hat.png', permanent = True)),
    url(r'^recentchanges',
        RedirectView.as_view(url='/+/?q=date:1W..', permanent = False)),
    url(r'^ikiwiki.cgi',
        RedirectView.as_view(url='/+/', permanent = False)),
   #url(r'piviti.xptv',
   #
    
    # Mess with script kiddies.
    url(r'^wp-', infinite_redirect),
    url(r'\.swf$', infinite_redirect),

    # Slashes
    url(r'^(.+[^/])$', lambda _, x: HttpResponseRedirect('/%s/' % x)),
)
