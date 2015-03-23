from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ..util import sh, direction

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run from any account with appropriate SSH keys.'

    def handle(self, *args, **options):
        direction('Run the tests.')
        direction('Copy canonical articles to nsa.')
        direction('Cache and index the articles on nsa.')
        direction('Copy ``pal.conf`` and pal calendar files to nsa.')
        direction('Generate static files on nsa.')
