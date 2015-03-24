import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from ..util import sh, direction

class Command(BaseCommand):
    args = '(none)'
    help = 'Get directions for installing.'

    def handle(self, *args, **options):
        template = get_template('install.md')
        with open(os.path.join(settings.BASE_DIR, 'requirements.txt')) as fp:
            requirements = [line.strip() for line in fp]
        d = {
            'requirements': requirements,
            'database': DATABASES['default']
            'notmuch_dir': os.path.join(settings.NOTMUCH_DB, 'mail'),
        }
        sys.stdout.write(template.render(Context(d)))
