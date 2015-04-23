from haystack import indexes

from .models import Message

class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_addr = 'datetime')
    title = indexes.CharField(model_addr = 'subject')
    _from = indexes.CharField(model_addr = '_from', index_fieldname = 'from')
    to = indexes.CharField(model_addr = 'to')
    cc = indexes.CharField(model_addr = 'cc')
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Message
