from django.conf import settings

from caching import SyncCommand

class Command(SyncCommand):
    plural_noun = '(unspecified plural noun)'
    directory = '(unspecified directory)'

    def discover(self, subdir = ()):
        '''
        subdir: Directory within ARTICLES_DIR to look
        endpoints: Endpoints that are already in the database
        '''
        parent = os.path.join(settings.ARTICLES_DIR, *subdir)

        # Process descendants
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if os.path.isdir(fn):
                yield from sync(subdir = subdir + (child,), threshold = threshold)
            elif not os.path.isfile(fn):
                logger.warning('Skipping %s because it is a symlink' % fn)
                continue

        # Process the present directory
        indices = [os.path.join(parent, child) for child in os.listdir(parent) if child.startswith('index.')]
        if len(indices) == 0:
            logger.debug('No index file in "%s"' % parent)
        elif len(indices) == 1:
            yield os.path.dirname(indices[0]), indices[0]
        elif len(indices) > 1:
            logger.debug('Several index files in "%s", using "%s"' % (parent, indices[0]))
            yield os.path.dirname(indices[0]), indices[0]
