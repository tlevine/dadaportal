import time, json

from django.db.models import Max
from django.db import models
from django.utils import timezone

from .reify import reify

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

    def head(self):
        return json.loads(self.headjson)

    def __str__(self):
        return self.endpoint

    @classmethod
    def sync(Klass, article_dir):
        threshold = Klass.objects.all().aggregate(Max('modified'))
        for topdir in os.listdir(article_dir):
            endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
            for endpoint in endpoints:
                fn = os.path.join(article_dir, endpoint) + '/'
                modified = datetime.datetime.fromtimestamp(os.stat(fn).st_mtime)
                if modified > threshold:
                    data = reify(article_dir, endpoint)
                    data['modified'] = modified
                    data['headjson'] = json.dumps(data['head'])
                    del(data['head'])
                    data['endpoint'] = endpoint
                    Klass.objects.create(**data)
