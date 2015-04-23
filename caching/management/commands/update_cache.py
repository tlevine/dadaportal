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
        # Populate the pks cache.
        pks = set(row[0] for row in Class.objects.values_list('pk'))

        # Update and create.
        n = 0
        for pk, fn in Class.discover():
            if pk in pks:
                self.stdout.write('Updated "%s"' % pk)
            else:
                self.stdout.write('Created "%s"' % pk)
            n += 1
        self.stdout.write('Created or updated %d %s' % (n, Class.plural_noun))
