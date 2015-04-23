import json
from urllib.parse import urljoin

from django.db import models

from caching import Cache

from .reify import reify as _reify

class Article(Cache):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    endpoint = models.TextField(null = False, blank = False)

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

    @property
    def tags(self):
        return json.loads(self.tagsjson)

    @tags.setter
    def tags(self, value):
        self.tagsjson = json.dumps(value)

    def __str__(self):
        return self.head().get('title', self.endpoint)

    @staticmethod
    def discover(subdir = ()):
        '''
        subdir: Directory within ARTICLES_DIR to look for new articles
        '''
        parent = os.path.join(settings.ARTICLES_DIR, *subdir)

        # Process descendants
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if os.path.isdir(fn):
                yield from self.discover(subdir = subdir + (child,))
            elif not os.path.isfile(fn):
                logger.warning('Skipping %s because it is a symlink' % fn)
                continue

        # Process the present directory
        indices = [os.path.join(parent, child) for child in os.listdir(parent) if child.startswith('index.')]
        if len(indices) == 0:
            logger.debug('No index file in "%s"' % parent)
        elif len(indices) == 1:
            yield indices[0]
        elif len(indices) > 1:
            logger.debug('Several index files in "%s", using "%s"' % (parent, indices[0]))
            yield indices[0]

    @staticmethod
    def reify(filename):
        return _reify(filename)
