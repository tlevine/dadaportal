import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from ..util import sh, direction

class Command(BaseCommand):
    args = '(none)'
    help = 'Generate an installation script to be run on the server.'

    def handle(self, *args, **options):
        template = get_template('install.sh')
        with open(os.path.join(settings.BASE_DIR, 'requirements.txt')) as fp:
            requirements = [line.strip() for line in fp]
        
        
        direction('Set up the database on nsa.')
        direction('Install, configure and enable the Apache site on nsa.')
        d = {
            'requirements': requirements,
            'database': DATABASES['default']
            'notmuch_dir': os.path.join(settings.NOTMUCH_DB, 'mail'),
        }

        sys.stdout.write(template.render(Context(d)))
