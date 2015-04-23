from urllib.parse import urljoin
import operator, os, datetime
from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect
from django.db.models import Q

from ..caching import get

from .reify import from_file, from_db
from .models import Article

def article(request, endpoint):
    try:
        obj = get(endpoint)
    except Article.DoesNotExist:
        raise Http404('Article is not cached in the database or doesn\'t exist at all.')

    if obj.redirect != None:
        return HttpResponseRedirect(obj.redirect)

    params = {
        'title': obj.title,
        'description': obj.description,
        'body': obj.body,
        'tags': obj.tags(),

        'facebook_title': obj.facebook_title,
        'facebook_description': obj.facebook_description,
        'facebook_image': obj.facebook_image,

        'twitter_title': obj.twitter_title,
        'twitter_description': obj.twitter_description,
        'twitter_image': obj.twitter_image,
    }
    return render(request, 'articles/article.html', params)

def index(request):
    articles = [{'endpoint': a.endpoint, 'title': a.title} for a in ArticleTag.objects.all()]
    return render(request, 'article/index.html', {'articles': articles})
