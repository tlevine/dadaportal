from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import ArticleCache

class Command(BaseCommand):
    args = '(none)'
    help = 'Loads articles from files in the %s directory' % settings.ARTICLES_DIR

    def handle(self, *args, **options):
        n = 0
        for endpoint in ArticleCache.sync():
            self.stdout.write('Updated "%s"' % endpoint)
            n += 1
        self.stdout.write('Updated %d articles' % n)
