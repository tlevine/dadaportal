from urllib.parse import urljoin
import operator, os, datetime
from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic.list import ListView

from caching import get

from .models import Article
from .big import guess_slides

def article(request, endpoint):
    try:
        obj = get(Article, endpoint = endpoint)
    except Article.DoesNotExist:
        raise Http404('Article is not cached in the database or doesn\'t exist at all.')
    return _article(request, obj)

def _article(request, obj):
    if obj.redirect != None:
        return HttpResponseRedirect(obj.redirect)

    if 'slides' in request.GET:
        template = 'articles/big.html'
        body = guess_slides(obj.body)
    else:
        template = 'articles/article.html'
        body = obj.body

    params = {
        'title': obj.title,
        'description': obj.description,
        'modified': obj.modified,
        'body': body,
        'tags': obj.tags,

        'facebook_title': obj.facebook_title,
        'facebook_description': obj.facebook_description,
        'facebook_image': urljoin(request.path_info, obj.facebook_image),

        'twitter_title': obj.twitter_title,
        'twitter_description': obj.twitter_description,
        'twitter_image': urljoin(request.path_info, obj.twitter_image),

        'source': os.path.relpath(obj.filename, settings.ARTICLES_DIR),
        'model': obj,
    }
    return render(request, template, params)

class IndexView(ListView):
    queryset = Article.objects.filter(redirect__isnull = True, secret = False)
    ordering = ('-modified',)
