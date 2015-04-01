import json
from urllib.parse import urljoin

from django.conf import settings
from django.db import models

class ArticleCache(models.Model):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    endpoint = models.TextField(primary_key = True)
    filename = models.TextField()
    modified = models.DateTimeField()
    headjson = models.TextField() # JSON
    body = models.TextField() # HTML

    def get_absolute_url(self):
        return '/!/%s/' % self.endpoint

    def head(self):
        return json.loads(self.headjson)

    def __str__(self):
        return self.head().get('title', self.endpoint)
