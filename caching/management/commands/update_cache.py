from django.core.management.base import BaseCommand
from django.db.models.loading import get_models

from ...models import Cache

class Command(BaseCommand):
    args = '(none)'
    help = 'Refreshes the database cache of file-backed Dada'

    def handle(self, *args, **options):
        for Model in get_models():
            if issubclass(Model, Cache):
                self.handle_one(Model)
        
    def handle_one(self, Class):
        # Populate the pks cache.
        filenames = set(row[0] for row in Class.objects.values_list('filename'))

        # Update and create.
        n = 0
        for filename in Class.discover():
            if filename in filenames:
                self.stdout.write('Updated "%s"' % filename)
            else:
                self.stdout.write('Created "%s"' % filename)
            n += 1
        self.stdout.write('Created or updated %d %s' % (n, Class.plural_noun))
