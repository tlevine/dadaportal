from haystack import indexes

from .models import Message

class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(model_attr = 'datetime')
    title = indexes.CharField(model_attr = 'subject')
    from_ = indexes.CharField(model_attr = 'from_', index_fieldname = 'from')
    to = indexes.CharField(model_attr = 'to')
    cc = indexes.CharField(model_attr = 'cc')
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Message
