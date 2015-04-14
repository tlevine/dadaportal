import os, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from ...models import ArticleCache

notmuch_dir = os.path.join(settings.NOTMUCH_MAILDIR, 'article')

class Command(BaseCommand):
    args = '(none)'
    help = 'Index articles in the notmuch database at %s.' % notmuch_dir

    def handle(self, *args, **options):
        template = get_template('article-notmuch.html')
        if os.path.isdir(notmuch_dir):
            for thing in os.listdir(notmuch_dir):
                os.remove(os.path.join(notmuch_dir, thing))
            subprocess.Popen(['notmuch', 'new'], stdout = subprocess.PIPE).wait()
        for article in ArticleCache.objects.all():
            fn = os.path.join(notmuch_dir, article.endpoint.replace('/', '---'))
            dn = os.path.dirname(fn)
            os.makedirs(dn, exist_ok = True)
            with open(fn, 'w') as fp:
                d = article.head()
                d.update({
                    'endpoint': article.endpoint,
                    'modified': article.modified.ctime(),
                    'body': article.body,
                    'notmuch_secret': settings.NOTMUCH_SECRET,
                })
                fp.write(template.render(Context(d)))
        subprocess.Popen(['notmuch', 'new']).wait()
