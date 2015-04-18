import json, os, datetime, logging, shutil, subprocess, hashlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Max, Q

from ...reify import from_file
from ...models import ArticleCache, ArticleTag

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

def sync(subdir = (), threshold = None, endpoints = set()):
    if len(endpoints) == 0:
        endpoints.update(row[0] for row in ArticleCache.objects.values_list('endpoint'))

    if threshold == None:
        threshold = ArticleCache.objects.all().aggregate(Max('modified'))['modified__max']
    if threshold == None: # (still)
        threshold = settings.BEGINNING_OF_TIME

    parent = os.path.join(settings.ARTICLES_DIR, *subdir)

    # Process descendants
    for child in os.listdir(parent):
        fn = os.path.join(parent, child)
        if os.path.isdir(fn):
            yield from sync(subdir = subdir + (child,), threshold = threshold)
        elif not os.path.isfile(fn):
            logger.warning('Skipping %s because it is a symlink' % fn)
            continue

    # Web endpoint
    endpoint = os.path.relpath(parent, settings.ARTICLES_DIR)

    # Process the present directory
    indices = [os.path.join(parent, child) for child in os.listdir(parent) if child.startswith('index.')]
    if len(indices) == 0:
        logger.debug('No index file in "%s"' % parent)
    elif datetime.datetime.fromtimestamp(os.stat(indices[0]).st_mtime) <= threshold or endpoint not in endpoints:
        logger.debug('Index file "%s" is old, skipping' % indices[0])
    else:
        head, body, meta = from_file(parent)
        if head == None and body == None and meta == None:
            logger.warn('I could not reify "%s", so I skipped it.' % parent)
        else:
            for k, v in head.items():
                if isinstance(v, datetime.date):
                    head[k] = v.isoformat()

            article_cache = ArticleCache.objects.filter(endpoint = endpoint)
            path = os.path.join(settings.ARTICLES_DIR, endpoint, meta['filename'])
            md5sum = hashlib.md5(open(path, 'rb').read()).hexdigest()

            if article_cache.count() == 1:
                article_cache.filter(~Q(md5sum = md5sum)).update(
                    filename = child, redirect = head.get('redirect'),
                    md5sum = md5sum, modified = meta['modified'],
                    headjson = json.dumps(head), body = body)
            else:
                article_cache = ArticleCache.objects.create(
                    endpoint = endpoint,
                    filename = child, redirect = head.get('redirect'),
                    md5sum = md5sum, modified = meta['modified'],
                    headjson = json.dumps(head), body = body)

            for tag in head.get('tags', []):
                if ArticleTag.objects.filter(article = article_cache, tag = tag).count() == 0:
                    ArticleTag.objects.create(article = article_cache, tag = tag)

            yield endpoint
