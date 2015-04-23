from haystack import indexes
from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_addr = 'modified')
    title = indexes.CharField(model_addr = 'title')
    tags = MultiValueField()
    text = indexes.CharField(document = True, use_template = True)

    def get_absolute_url(self):
        return '/!/%s/' % self.endpoint

    def tags(self):
        return json.loads(self.tagsjson)

    def __str__(self):
        return self.head().get('title', self.endpoint)

    @staticmethod
    def discover(subdir = ()):
        '''
        subdir: Directory within ARTICLES_DIR to look for new articles
        '''
        parent = os.path.join(settings.ARTICLES_DIR, *subdir)

        # Process descendants
        for child in os.listdir(parent):
            fn = os.path.join(parent, child)
            if os.path.isdir(fn):
                yield from self.discover(subdir = subdir + (child,))
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

    @staticmethod
    def reify(filename):
        return _reify(filename)


    def get_model(self):
        return Article

    def prepare_tags(self, obj):
        return obj.tags()
