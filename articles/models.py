import json, os, logging
from urllib.parse import urljoin

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from caching import Cache

from .reify import reify as _reify

logger = logging.getLogger(__name__)

class Article(Cache):
    '''
    The canonical version of the article is stored in a file, but the
    articles are loaded from a cache so it can be more Django-like and
    so I thus don't have to think as much.
    '''
    endpoint = models.TextField(null = False, blank = False)

    title = models.TextField(null = True)
    description = models.TextField(null = True)
    body = models.TextField(null = False)

    redirect = models.TextField(null = True)
    tagsjson = models.TextField(null = False) # JSON

    facebook_title = models.TextField(null = True)
    facebook_description = models.TextField(null = True)
    facebook_image = models.TextField(null = True)

    twitter_title = models.TextField(null = True)
    twitter_description = models.TextField(null = True)
    twitter_image = models.TextField(null = True)

    def get_absolute_url(self):
        return reverse('articles/article', args = (self.endpoint,))

    @property
    def tags(self):
        return json.loads(self.tagsjson)

    @tags.setter
    def tags(self, value):
        self.tagsjson = json.dumps(value)

    @classmethod
    def discover(Class, subdir = ()):
        '''
        subdir: Directory within ARTICLES_DIR to look for new articles
        '''
        parent = os.path.join(settings.ARTICLES_DIR, *subdir)

        # Process descendants
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if child.startswith('.'):
                logger.debug('Skipping %s because it is hidden' % fn)
            elif os.path.isdir(fn):
                yield from Class.discover(subdir = subdir + (child,))
            elif not os.path.isfile(fn):
                logger.warning('Skipping %s because it is a symlink' % fn)

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

    def __str__(self):
        msg = '%(class)s "%(instance)s"'
        params = {
            'class': self.__class__.__name__,
            'instance': self.title if self.title else self.endpoint,
        }
        return msg % params
