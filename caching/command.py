from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class SyncCommand(BaseCommand):
    plural_noun = '(unspecified plural noun)'
    directory = '(unspecified directory)'

    args = '(none)'
    def help(self):
        return 'Loads %s from files in the %s directory' % (self.plural_noun, self.directory)

    def discover(self):
        raise NotImplementedError

    def handle(self, *args, **options):
        # Populate the endpoints cache.
        endpoints = set(row[0] for row in Article.objects.values_list('endpoint'))

        # Update and create.
        n = 0
        for endpoint, fn in self.discover():
            if endpoint in endpoints:
                self.stdout.write('Updated "%s"' % endpoint)
            else:
                self.stdout.write('Created "%s"' % endpoint)
            n += 1
        self.stdout.write('Created or updated %d %s' % (n, self.plural_noun))
