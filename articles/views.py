from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .models import ArticleCache

def article(request, endpoint):
    try:
        a = ArticleCache.objects.get(endpoint = endpoint)
    except ArticleCache.DoesNotExist:
        raise Http404('No such article')
    else:
        params = a.head()
        params['modified'] = a.modified
        params['body'] = a.body
        return render(request, 'article.html', params)
