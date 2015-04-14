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
    return _run(['rsync', '-avHS', '--exclude', 'static-compiled', '--exclude', '.*', local, r])

def scp(local, remote):
    r = '%s@%s:%s' % (settings.REMOTE_USER, settings.REMOTE_SSH_HOST, remote)
    return _run(['scp', local, r])

def scp_text(text, remote):
    with open('/tmp/ttttttt', 'w') as tmp:
        tmp.write(text)
    code = scp(tmp.name, remote)
    os.remove(tmp.name)
    return code

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

        self._comment('Copying pal calendar files to nsa')
        rsync(settings.LOCAL_PAL_DIR, settings.REMOTE_PAL_DIR)

        self._comment('Copying pal.conf to nsa')
        text = get_template('config/pal.conf').render(Context({}))
        scp_text(text, os.path.join(settings.REMOTE_PAL_DIR, 'pal.conf'))

        self._comment('Writing .notmuch-config to nsa')
        params = {
            'NOTMUCH_MAILDIR': settings.REMOTE_NOTMUCH_MAILDIR,
            'NAME': settings.NAME,
            'EMAIL_ADDRESS': settings.EMAIL_ADDRESS,
            'NOTMUCH_OTHER_EMAIL': settings.NOTMUCH_OTHER_EMAIL,
        }
        text = get_template('config/notmuch-config').render(Context(params))
        scp_text(text, os.path.join(settings.REMOTE_BASE_DIR, 'notmuch-config'))

        self._comment('Caching the articles on nsa')
        ssh('./manage.py syncarticles')

        self._comment('Indexing the articles on nsa')
        ssh('./manage.py indexarticles')

        self._comment('Generating static files on nsa')
        ssh('./manage.py collectstatic')

        self.stdout.write('''

Now reload apache, probably with this.

  service apache2 reload
''')
