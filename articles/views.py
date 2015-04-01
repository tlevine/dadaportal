import operator
from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.db.models import Q

from .models import ArticleTag, ArticleCache

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

def index(request):
    tags = request.GET.get('tags')
    if tags == None:
        query = ArticleTag.objects
    else:
        qs = reduce(operator.or_, (Q(tag = tag) for tag in tags.split('|')))
        query = ArticleTag.objects.filter(qs).select_related('article')
    articles = [article_tag.article for article_tag in query.distinct('article_id') if 'title' in article_tag.article.head()]
    articles_simple = [{'href': a.endpoint, 'title': a.head()['title']} for a in articles]
    return render(request, 'article-index.html', {'articles': articles_simple})
