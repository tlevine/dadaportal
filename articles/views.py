import operator, os, datetime
from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect
from django.db.models import Q

from .reify import from_file, from_db
from .models import ArticleTag, ArticleCache

def article_cached(request, endpoint):
    try:
        article_cache = ArticleCache.objects.get(endpoint = endpoint)
    except ArticleCache.DoesNotExist:
        raise Http404('Article is not cached in the database or doesn\'t exist at all.')
    else:
        return _article(request, *from_db(article_cache))

def article_canonical(request, endpoint):
    return _article(request, *from_file(os.path.join(settings.ARTICLES_DIR, endpoint)))

def _article(request, head, body, meta):
    if head == None and body == None and meta == None:
        msg = 'Could not reify %s' % request.path_info
        return HttpResponseServerError(content = msg.encode('utf-8'))
    elif meta['redirect'] != None:
        return HttpResponseRedirect(meta['redirect'])
    else:
        params = {'body': body}
        params.update(head)
        params.update(meta)
        return render(request, 'article.html', params)

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
