import json
from urllib.parse import urljoin

from caching import Cache

class Article(Cache):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    title = models.TextField(null = False)
    description = models.TextField(null = False)
    body = models.TextField(null = False)

    redirect = models.TextField(null = True)
    tagsjson = models.TextField(null = False) # JSON

    facebook_title = models.TextField(null = False)
    facebook_description = models.TextField(null = False)
    facebook_image = models.TextField(null = False)

    twitter_title = models.TextField(null = False)
    twitter_description = models.TextField(null = False)
    twitter_image = models.TextField(null = False)

    def get_absolute_url(self):
        return '/!/%s/' % self.endpoint

    def tags(self):
        return json.loads(self.tagsjson)

    def __str__(self):
        return self.head().get('title', self.endpoint)

    @staticmethod
    def reify(filename):
        return _reify(filename)
