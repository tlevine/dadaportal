from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dadaportal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#   url(r'^\+/', include('search.urls')),
#   url(r'^@/', include('mail.urls')),
    url(r'^!/', include('articles.urls')),

    # Static
   #url(r'^static/',
   #url(r'^img/.+', RedirectView.as_view(url='/static/img/')
   #url(r'^!/[^/]/.+', 
)
