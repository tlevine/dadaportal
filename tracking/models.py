#https://docs.djangoproject.com/en/dev/topics/http/sessions/
from django.db import models

class Hit(models.Model):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'

    # Populated on the first request
    id = models.BigIntegerField(primary_key = True)
    session = models.Field(null = False)
    datetime = models.Field(s.DateTime, null = False)
    ip_address = models.Field(null = False)
    user_agent = models.Field(s.String, null = False)
    referrer = models.Field(s.String, null = False) # blank if none

    # Populated on the subsequent XHR, updated every few seconds
    screen_width = models.Field(s.Integer, null = True)
    screen_height = models.Field(s.Integer, null = True)
    seconds_on_page = models.Field(s.Integer, null = True)

    def insert_primary():
        pass

    def insert_js():
        pass

class ArticleHitCounts(models.Model):
    '''
    This table has a row for each article and hour, and a column for hit
    counts for the past few days. It can be generated fully the contents
    of the "hit" table.
    '''
    __tablename__ = 'article_statistics'

    # With the trailing slash
    endpoint = models.TextField(primary_key = True)

    day_0 = models.IntegerField(null = False) # today
    day_1 = models.IntegerField(null = False) # yesterday
    day_2 = models.IntegerField(null = False)
    day_3 = models.IntegerField(null = False)
    day_4 = models.IntegerField(null = False)
    day_5 = models.IntegerField(null = False)
    day_6 = models.IntegerField(null = False) # a week ago, rounded down
    day_7 = models.IntegerField(null = False) # a week ago, rounded up

    @classmethod
    def shift(Klass):
        'Klass.day_7 is set to Klass.day_6, and so on.'
        pass


class Search(models.Model):
    '''
    This table has a row for each article and a column for each of several
    statistics. It can be generated fully from the contents of the "hit" table.
    '''
    __tablename__ = 'search'
    hit = models.BigIntegerField(primary_key = True)
    terms = models.TextField(null = False)
    email_only = models.BooleanField(null = False)
    n_results = models.IntegerField(null = False)
