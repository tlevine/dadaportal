import os, subprocess, sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

SH_MESSAGE = '''You are about to run this command.

    $ %s

Are you sure you want to run it? Hit enter if yes.
'''
def sh(command):
    sys.stdout.write(SH_MESSAGE % command)
    input()
    p = subprocess.Popen(command.split(), stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    p.wait()
    return p.stdout.read()

def direction(command):
    sys.stdout.write(command.strip() + '\n')
    input()

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run as the web user on the server.'

    def handle(self, *args, **options):
        raise CommandError('This should be run on the web server.')


        # Create a user with the appropriate home directory and group.
        sh('sudo createuser %s' % settings.WEB_USER)
        
        direction('''
Install this crontab to send public emails from the email server (home)
to nsa; you must copy it to the computer that contains your emails.''')

* Set up the database on nsa.
* Install, configure and enable the Apache site on nsa.
* Install dependencies on nsa

  * Python libraries
  * pal
  * notmuch
