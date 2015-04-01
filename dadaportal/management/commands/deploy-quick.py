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
    return _run(['rsync', '-avHS', '--exclude', '.*', local, r])

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

        self._comment('Copying the local repository to nsa')
        rsync('.', settings.REMOTE_BASE_DIR)

        self.stdout.write('''

Now reload apache, probably with this.

  service apache2 reload
''')
