import time, json, os, datetime, logging
import subprocess
from urllib.parse import urljoin

from django.conf import settings
from django.db.models import Max
from django.db import models
from django.utils import timezone
from django.template.loader import get_template
from django.template import Context

from .reify import reify

logger = logging.getLogger(__name__)

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
        return '/!/%s/' % self.endpoint

    def head(self):
        return json.loads(self.headjson)

    def __str__(self):
        return self.head().get('title', self.endpoint)

    @classmethod
    def sync(Klass, subdir = (), threshold = None):
        if threshold == None:
            threshold = Klass.objects.all().aggregate(Max('modified'))['modified__max']
        if threshold == None: # (still)
            threshold = settings.BEGINNING_OF_TIME

        parent = os.path.join(settings.ARTICLES_DIR, *subdir)
        indexes = 0
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if os.path.isdir(fn):
                yield from Klass.sync(subdir = subdir + (child,), threshold = threshold)
            elif child.startswith('index.'):
                if indexes > 0:
                    logger.warn('There were multiple index files for %s, so I used only the first one' % parent)
                    continue
                indexes += 1
                modified = datetime.datetime.fromtimestamp(os.stat(fn).st_mtime)
                if modified > threshold:
                    endpoint = os.path.dirname(os.path.relpath(fn, settings.ARTICLES_DIR))
                    head, body = reify(settings.ARTICLES_DIR, fn)
                    if head == None and body == None:
                        logger.warn('I could not reify %s, so I skipped it.' % endpoint)
                    else:
                        article_cache, already_exists = Klass.objects.get_or_create(
                            endpoint = endpoint, modified = modified,
                            headjson = json.dumps(head), body = body)
                        yield endpoint

    @classmethod
    def index(Klass):
        template = get_template('article-notmuch.html')
        for article in Klass.objects.all():
            fn = os.path.join(settings.NOTMUCH_DB, article.endpoint.replace('/', '---'))
            dn = os.path.dirname(fn)
            if not os.path.isdir(dn):
                os.makedirs(dn)
            with open(fn, 'w') as fp:
                d = article.head()
                d.update({
                    'endpoint': article.endpoint,
                    'modified': article.modified.ctime(),
                    'body': article.body,
                    'notmuch_secret': settings.NOTMUCH_SECRET,
                })
                fp.write(template.render(Context(d)))
        subprocess.Popen(['notmuch', 'new'])
