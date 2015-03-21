import time, json

from django.db import models
from django.utils import timezone

class StickyNote(models.Model):
    '''
    Small things to remember
    '''
    key = models.TextField(primary_key = True)
    value = model.TextField()

class ArticleCache(models.Model):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    endpoint = models.TextField(primary_key = True)
    headjson = models.TextField() # JSON
    body = model.TextField() # HTML

    def head(self):
        return json.loads(self.headjson)

    def __str__(self):
        return self.endpoint

    @classmethod
    def sync(Klass, article_dir):
        sync_date = StickyNote.objects.get_or_create(key = 'article_sync_date')
        prev_sync = float(sync_date.value)
        for topdir in os.listdir(article_dir):
            endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
            for endpoint in endpoints:
                fn = os.path.join(article_dir, endpoint) + '/'
                modified = os.stat(fn).st_mtime
                if modified > prev_sync:
                    data = reify(article_dir, endpoint)
                    data['headjson'] = json.dumps(data['head'])
                    del(data['head'])
                    data['endpoint'] = endpoint
                    Klass.objects.create(**data)
        sync_date.value = str(time.time())
        sync_date.save()
