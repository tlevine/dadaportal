from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import ArticleCache

class Command(BaseCommand):
    args = '(none)'
    help = 'Index articles in the notmuch database at %s.' % settings.NOTMUCH_DB

    def handle(self, *args, **options):
        ArticleCache.index()
