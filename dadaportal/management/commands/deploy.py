from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

def _run(args):
    p = subprocess.Popen(args, stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    p.wait()
    return p

def rsync(local, remote):
    return _run(['rsync', local, settings.REMOTE_HOST + ':' + remote])

def rsync_text(text, remote):
    with tempfile.NamedTemporaryFile(mode = 'w') as tmp:
        tmp.write(text)
    return rsync(tmp.name, remote)

def ssh(command):
    full_command = "cd '%s' && %s" % (settings.REMOTE_BASE_DIR, command)
    return _run(['ssh', settings.REMOTE_HOST, full_command])

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

        self.stdout.write('Copying pal calendar files to nsa')
        rsync(settings.LOCAL_PAL_DIR, settings.REMOTE_PAL_DIR)

        self.stdout.write('Copy pal.conf to nsa')
        text = get_template('config/pal.conf').render()
        rsync_text(text, os.path.join(settings.REMOTE_PAL_DIR, 'pal.conf'))

        self.stdout.write('Generating static files on nsa')
        ssh('./manage.py collectstatic')
