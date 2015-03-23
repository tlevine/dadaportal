import json, os, datetime, logging, shutil, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Max

from ...reify import reify
from ...models import ArticleCache

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '(none)'
    help = 'Loads articles from files in the %s directory' % settings.ARTICLES_DIR

    def handle(self, *args, **options):
        n = 0
        for endpoint in sync():
            self.stdout.write('Updated "%s"' % endpoint)
            n += 1
        self.stdout.write('Updated %d articles' % n)

def sync(subdir = (), threshold = None):
    if threshold == None:
        threshold = ArticleCache.objects.all().aggregate(Max('modified'))['modified__max']
    if threshold == None: # (still)
        threshold = settings.BEGINNING_OF_TIME

    parent = os.path.join(settings.ARTICLES_DIR, *subdir)
    indexes = 0
    for child in os.listdir(parent):
        fn = os.path.join(parent, child)
        if os.path.isdir(fn):
            yield from sync(subdir = subdir + (child,), threshold = threshold)
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
                    if ArticleCache.objects.filter(endpoint = endpoint).count() == 1:
                        ArticleCache.objects.filter(endpoint = endpoint).update(
                            modified = modified, headjson = json.dumps(head), body = body)
                    else:
                        article_cache = ArticleCache.objects.get_or_create(
                            endpoint = endpoint, modified = modified,
                            headjson = json.dumps(head), body = body)
                    yield endpoint
