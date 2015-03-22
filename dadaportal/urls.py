from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dadaportal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^\+$', RedirectView.as_view(url='/+/')),
    url(r'^\+/$', 'search.views.search'),

    url(r'^@/', include('mail.urls')),

    url(r'^!/', include('articles.urls')),

    # Static
   #url(r'^static/',
   #url(r'^img/.+', RedirectView.as_view(url='/static/img/')
)
