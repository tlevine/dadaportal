from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import ArticleCache

class Command(BaseCommand):
    args = '(none)'
    help = 'Loads articles from files in the %s directory' % settings.ARTICLES_DIR

    def handle(self, *args, **options):
        for i, endpoint in enumerate(ArticleCache.sync()):
            self.stdout.write('Updated "%s"' % endpoint)
        self.stdout.write('Updated %d articles' % i + 1)
