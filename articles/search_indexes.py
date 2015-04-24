from haystack import indexes

from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_attr = 'modified')
    title = indexes.CharField(model_attr = 'title')
    description = indexes.CharField(indexed = False)
    tags = indexes.MultiValueField(model_attr = 'tags')
    text = indexes.CharField(document = True, use_template = True, stored = False)

    def get_model(self):
        return Article

    def prepare_description(self, obj):
        return obj.description if obj.description else ''
