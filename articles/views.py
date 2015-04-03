import operator, os, datetime
from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect
from django.db.models import Q

from .reify import reify
from .models import ArticleTag, ArticleCache

def article_cached(request, endpoint):
    try:
        a = ArticleCache.objects.get(endpoint = endpoint)
    except ArticleCache.DoesNotExist:
        raise Http404('No such article')

    if a.redirect == None:
        params = a.head()
        params['modified'] = a.modified
        params['body'] = a.body
        params['filename'] = a.filename
        params['endpoint'] = a.endpoint
        return render(request, 'article.html', params)
    else:
        return HttpResponseRedirect(a.redirect)


def article_canonical(request, endpoint):
    dn = os.path.join(settings.ARTICLES_DIR, endpoint)
    for just_fn in os.listdir(dn):
        if just_fn.startswith('index.'):
            fn = os.path.join(dn, just_fn)
            break
    else:
        raise Http404('No such article')
    head, body = reify(settings.ARTICLES_DIR, fn)
    if head == None and body == None:
        msg = 'Could not reify %s' % fn
        return HttpResponseServerError(content = msg.encode('utf-8'))
    elif 'redirect' in head:
        return HttpResponseRedirect(head['redirect'])
    else:
        params = dict(head)
        params['modified'] = datetime.date.today()
        params['body'] = body
        params['filename'] = just_fn
        params['endpoint'] = endpoint
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
