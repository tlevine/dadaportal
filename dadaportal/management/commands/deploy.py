import subprocess, tempfile, sys, shlex, os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

def _run(args):
    sys.stdout.write(' '.join(map(shlex.quote, args)) + '\n')
    if 0 != subprocess.call(args):
        sys.exit(1)

def rsync(local, remote):
    r = '%s@%s:%s' % (settings.REMOTE_USER, settings.REMOTE_SSH_HOST, remote)
    return _run(['rsync', '-avHS', '--delete', '--exclude', '.*', local, r])

def ssh(command, prefix = True):
    if prefix:
        full_command = "cd '%s' && %s" % (settings.REMOTE_BASE_DIR, command)
    else:
        full_command = command
    r = '%s@%s' % (settings.REMOTE_USER, settings.REMOTE_SSH_HOST)
    return _run(['ssh', r, full_command])

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run from any account with appropriate SSH keys.'

    def _comment(self, x):
        self.stdout.write('# ' + x)

    def handle(self, *args, **options):
        if settings.IS_PRODUCTION:
            raise CommandError('This command should be run from the development system, not from production.')

       #self._comment('Running tests')
       #_run(['./manage.py', 'test'])

        self._comment('Creating the remote base directory')
        ssh('mkdir -p \'%s\'' % settings.REMOTE_BASE_DIR, prefix = False)

        self._comment('Copying the local repository to nsa')
        rsync('.', settings.REMOTE_BASE_DIR)

        self.stdout.write('''
If this is the first time you ran "./manage deploy", log into the
server (ssh www-data@nsa) and run the following.

$ ./manage.py syncdb

If you have changed the database schema, run this,

$ ./manage.py makemigrations
$ ./manage.py migrate

and then copy the migrations into the repository on your non-server
computer.''')

#       self._comment('Copying pal calendar files to nsa')
#       rsync(settings.LOCAL_PAL_DIR, settings.REMOTE_PAL_DIR)

        self._comment('Updating the cache')
        ssh('./manage.py update_cache')

        self._comment('Updating the search index')
        ssh('./manage.py update_index')

        self._comment('Generating static files on nsa')
        ssh('./manage.py collectstatic --noinput')

        self.stdout.write('''

Now reload apache, probably with this.

  service apache2 reload
''')
