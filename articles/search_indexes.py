from haystack import indexes
from .models import ArticleCache

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_addr = 'modified')
    title = indexes.CharField()
    tags = MultiValueField()
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return ArticleCache

    def prepare_tags(self, obj):
        return obj.head().get('tags', [])

    def prepare_title(self, obj):
        return obj.head().get('title', '')
