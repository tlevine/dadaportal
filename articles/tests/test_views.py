import datetime

import pytest
from django.test import Client, RequestFactory
from django.template.loader import render_to_string
from django.template import RequestContext

from ..models import Article
from ..views import _article

@pytest.mark.django_db
def test_index():
    'GET /!/ should return a list of articles.'
    Article.objects.create(filename = 'a/b/index.md', endpoint = 'a/b',
        modified = datetime.datetime.now(), md5sum = 'abc', title = 'Schaufelradbagger')
    c = Client()
    response = c.get('/!/')
    assert b'<a href="/!/a/b/">Schaufelradbagger</a>' in response.content

def test_article():
    a = Article(
        endpoint = 'aa/bb',
        md5sum = 'xxx',
        modified = datetime.datetime.now(),

        title = 'AAA',
        description = 'BBB',
        body = '<p>Body here</p>',
        tags = ['tag1', 'tag2'],
        facebook_title = 'CCC',
        facebook_description = 'DDD',
        facebook_image = 'EEE',

        twitter_title = 'FFF',
        twitter_description = 'GGG',
        twitter_image = 'HHH')

    f = RequestFactory()
    request = f.get('/!/aa/bb/')
    request.hit_id = 8
    request.session = {'session_id': 9}
    response = _article(request, a)

    # Test that stuff is in here.
    response.content

def test_article_defaults():
    a = Article(
        endpoint = 'aa/bb',
        md5sum = 'xxx',
        modified = datetime.datetime.now(),
        body = '<p>Body here</p>',
        tags = [])

    f = RequestFactory()
    request = f.get('/!/aa/bb/')
    request.hit_id = 8
    request.session = {'session_id': 9}
    response = _article(request, a)

    # Test that stuff is in here.
    response.content
