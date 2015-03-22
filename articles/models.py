import time, json, os, datetime
from urllib.parse import urljoin

from django.conf import settings
from django.db.models import Max
from django.db import models
from django.utils import timezone

from .reify import reify

BEGINNING_OF_TIME = datetime.datetime(1990, 3, 30)

class ArticleCache(models.Model):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    endpoint = models.TextField(primary_key = True)
    modified = models.DateTimeField()
    headjson = models.TextField() # JSON
    body = models.TextField() # HTML

    def get_absolute_url(self):
        return urljoin('/', self.endpoint)

    def head(self):
        return json.loads(self.headjson)

    def __str__(self):
        return self.head().get('title', self.endpoint)

    @classmethod
    def sync(Klass, subdir = ()):
        threshold = Klass.objects.all().aggregate(Max('modified'))['modified__max']
        if threshold == None:
            threshold = BEGINNING_OF_TIME
        parent = os.path.join(settings.ARTICLES_DIR, *subdir)
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if os.path.isdir(fn):
                yield from Klass.sync(subdir = subdir + (child,))
            elif child.startswith('index.'):
                modified = datetime.datetime.fromtimestamp(os.stat(fn).st_mtime)
                if modified > threshold:
                    head, body = reify(settings.ARTICLES_DIR, fn)
                    endpoint = os.path.dirname(os.path.relpath(fn, settings.ARTICLES_DIR))
                    data = {
                        'endpoint': endpoint,
                        'modified': modified,
                        'headjson': json.dumps(head),
                        'body': body,
                    }
                    Klass.objects.create(**data)
                    yield endpoint
                break
