import datetime

from django.db import models

class Hit(models.Model):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'

    # Populated on the first request
    id = models.BigIntegerField(primary_key = True)
    session = models.BigIntegerField(null = False)
    datetime = models.DateTimeField(null = False, default = datetime.datetime.now)
    endpoint = models.TextField(null = False)
    ip_address = models.IPAddressField(null = False)
    user_agent = models.TextField(null = False)
    referrer = models.URLField(null = False)

    # Populated on the subsequent XHR, updated every few seconds
    fresh = models.BooleanField(null = False, default = True)
    screen_width = models.Field(null = True)
    screen_height = models.Field(null = True)
    seconds_on_page = models.Field(null = True)

class ArticleHitCounts(models.Model):
    '''
    This table has a row for each article and hour, and a column for hit
    counts for the past few days. It can be generated fully the contents
    of the "hit" table.
    '''
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
        for i in reversed(range(1, 8)):
            yesterday = 'day_%d' % i
            today = 'day_%d' % (i - 1)
            kwargs = {yesterday: models.F(today)}
            Klass.objects.all().update(**kwargs)

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
