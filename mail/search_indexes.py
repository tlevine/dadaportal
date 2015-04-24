from haystack import indexes

from .models import Message

class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_attr = 'datetime')
    url = indexes.CharField(model_attr = 'endpoint')
    title = indexes.CharField(model_attr = 'subject')
    ffrom = indexes.CharField(model_attr = 'ffrom', index_fieldname = 'from')
    to = indexes.CharField(model_attr = 'to')
    cc = indexes.CharField(model_attr = 'cc')

    url = indexes.CharField(model_attr = 'message_id')
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Message

    def prepare_url(self, obj):
        return obj.get_absolute_url()
