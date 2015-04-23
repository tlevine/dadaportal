from haystack import indexes

from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_addr = 'modified')
    title = indexes.CharField(model_addr = 'title')
    tags = MultiValueField(model_addr = 'tags')
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Article
