from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

def _run(args):
    p = subprocess.Popen(args, stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    p.wait()
    return p

def rsync(local, remote, remote_host = 'nsa'):
    return _run(['rsync', local, remote_host + ':' + remote])

def ssh(command, remote_host = 'nsa'):
    full_command = "cd '%s' && %s" % (settings.REMOTE_BASE_DIR, command)
    return _run(['ssh', remote_host, full_command])

class Command(BaseCommand):
    args = '(none)'
    help = 'This should be run from any account with appropriate SSH keys.'

    def handle(self, *args, **options):
        self.stdout.write('Running tests')
        _run(['./manage.py', 'test'])

        self.stdout.write('Copying canonical articles to nsa')
        # no slash at end of remote directory
        rsync('./canonical-articles/', '%s/canonical-articles' % settings.REMOTE_BASE_DIR)

        self.stdout.write('Caching the articles on nsa')
        ssh('./manage.py syncarticles')

        self.stdout.write('Indexing the articles on nsa')
        ssh('./manage.py indexarticles')

        self.stdout.write('Copy pal.conf to nsa')
        rsync(settings.LOCAL_PAL_CONF, settings.REMOTE_PAL_CONF)

        self.stdout.write('Copying pal calendar files to nsa')
        rsync(settings.LOCAL_PAL_DIR, settings.REMOTE_PAL_DIR)

        self.stdout.write('Generating static files on nsa')
        ssh('./manage.py collectstatic')
