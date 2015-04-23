import datetime

import pytest
from django.test import Client

@pytest.mark.django_db
def test_index():
    'GET /!/ should return a list of articles.'
    Article.objects.create(filename = 'a/b/index.md', endpoint = 'a/b',
        modified = datetime.datetime.now(), md5sum = 'abc', title = 'Schaufelradbagger')
    c = Client()
    response = c.get('/!/')
    assert '"a/b/">Schaufelradbagger</a>' in response.content