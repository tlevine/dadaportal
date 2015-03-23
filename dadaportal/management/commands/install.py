from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ..util import sh, direction

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run as the web user on the server.'

    def handle(self, *args, **options):
        raise CommandError('This should be run on the web server.')

        direction('''Install dependencies on nsa.
  * Python libraries
  * pal
  * notmuch
''')

        # Create a user with the appropriate home directory and group.
        sh('sudo createuser %s' % settings.WEB_USER)
        
        direction('''
Install this crontab to send public emails from the email server (home)
to nsa; you must copy it to the computer that contains your emails.''')

        direction('Set up the database on nsa.')
        direction('Install, configure and enable the Apache site on nsa.')
