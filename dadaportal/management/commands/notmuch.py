import subprocess, tempfile, sys, shlex, os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run from any account with appropriate SSH keys.'

    def handle(self, *args, **options):
        params = {
            'NOTMUCH_MAILDIR': settings.NOTMUCH_MAILDIR,
            'NAME': settings.NAME,
            'EMAIL_ADDRESS': settings.EMAIL_ADDRESS,
            'NOTMUCH_OTHER_EMAIL': settings.NOTMUCH_OTHER_EMAIL,
        }
        text = get_template('config/.notmuch-config').render(Context(params))
        with open(os.environ['NOTMUCH_CONFIG'], 'w') as fp:
            fp.write(text)
