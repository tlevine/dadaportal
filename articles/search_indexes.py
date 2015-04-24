from haystack import indexes
from django.conf import settings

from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_attr = 'modified')
    title = indexes.CharField(model_attr = 'title')
    tags = indexes.MultiValueField(model_attr = 'tags')

    url = indexes.CharField(model_attr = 'endpoint')
    text = indexes.CharField(document = True, use_template = True, stored = False)
    description = indexes.CharField(indexed = False)

    def get_model(self):
        return Article

    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def prepare_description(self, obj):
        return obj.description if obj.description else settings.EMPTY_SEARCH_DESCRIPTION
