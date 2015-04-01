from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

from .models import ArticleCache

def article(request, endpoint):
    try:
        a = ArticleCache.objects.get(endpoint = endpoint)
    except ArticleCache.DoesNotExist:
        raise Http404('No such article')

    if a.redirect == None:
        params = a.head()
        params['modified'] = a.modified
        params['body'] = a.body
        return render(request, 'article.html', params)
    else:
        return HttpResponseRedirect(a.redirect)
