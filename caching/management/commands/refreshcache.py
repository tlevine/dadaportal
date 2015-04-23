from django.core.management.base import BaseCommand
from django.db.models.loading import get_models

from ...models import Cache

class Command(BaseCommand):
    args = '(none)'
    help = 'Refreshes the database cache of file-backed Dada'

    def discover(self):
        raise NotImplementedError

    def handle(self, *args, **options):
        for Model in get_models():
            if issubclass(Model, Cache):
                self.handle_one(Model)
        
    def handle_one(self, Class):
        # Populate the endpoints cache.
        endpoints = set(row[0] for row in Class.objects.values_list('endpoint'))

        # Update and create.
        n = 0
        for endpoint, fn in self.discover():
            if endpoint in endpoints:
                self.stdout.write('Updated "%s"' % endpoint)
            else:
                self.stdout.write('Created "%s"' % endpoint)
            n += 1
        self.stdout.write('Created or updated %d %s' % (n, Class.plural_noun))
