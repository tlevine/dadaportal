from haystack import indexes

from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_attr = 'modified')
    title = indexes.CharField(model_attr = 'title')
    tags = indexes.MultiValueField(model_attr = 'tags')
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Article
