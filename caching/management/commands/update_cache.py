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
            if filename not in filenames:
                obj = Class.add(filename)
                self.stdout.write('Created %s' % obj)
                n += 1
                continue

            obj = Class.objects.get(filename = filename)
            if obj.sync():
                self.stdout.write('Updated %s' % obj)
                n += 1
                continue

        self.stdout.write('Created or updated %d %s records' % (n, Class.__name__))
