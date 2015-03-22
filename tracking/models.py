import datetime

from django.db import models

class Hit(models.Model):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'

    # Populated on the first request
    id = models.BigIntegerField(primary_key = True)
    session = models.BigIntegerField(null = False)
    datetime_start = models.DateTimeField(null = False, default = datetime.datetime.now)
    endpoint = models.TextField(null = False)
    ip_address = models.IPAddressField(null = False)
    user_agent = models.TextField(null = False)
    referrer = models.URLField(null = False)

    # Populated on the subsequent XHR, updated every few seconds
    screen_width = models.IntegerField(null = True)
    screen_height = models.IntegerField(null = True)
    datetime_end = models.DateTimeField(null = True)

class Search(models.Model):
    '''
    This table has a row for each article and a column for each of several
    statistics. It can be generated fully from the contents of the "hit" table.
    '''
    hit = models.ForeignKey(Hit, primary_key = True)
    terms = models.TextField(null = False)
    email_only = models.BooleanField(null = False)
    n_results = models.IntegerField(null = False)
