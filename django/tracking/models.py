import datetime

from django.db import models

class Hit(models.Model):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'

    # Populated on the first request
    hit = models.BigIntegerField(primary_key = True)
    session = models.BigIntegerField(null = False, blank = False)
    datetime_start = models.DateTimeField(null = False, default = datetime.datetime.now)
    endpoint = models.TextField(null = False, blank = False)
    querystring = models.TextField(null = False)
    ip_address = models.GenericIPAddressField(null = False, blank = False)
    accept_language = models.TextField(null = False)
    user_agent = models.TextField(null = False)

    # high max_length to support facebook urls
    referrer = models.URLField(null = False, max_length = 10000)

    # Populated after the response (maybe during the XHR if that's easier)
    status_code = models.SmallIntegerField(null = True)

    # Populated on the subsequent XHR, updated every few seconds
    datetime_end = models.DateTimeField(null = True)
    availWidth = models.IntegerField(null = True)
    availHeight = models.IntegerField(null = True)
    scrollX = models.IntegerField(null = True)
    scrollY = models.IntegerField(null = True)
    pageXOffset = models.IntegerField(null = True)
    pageYOffset = models.IntegerField(null = True)

    # Populated on the XHR or the img
    javascript_enabled = models.NullBooleanField()

    def __str__(self):
        d = self.datetime_start.strftime('%B %d, %H:%M:%S')
        return '%d (%s at %s)' % (self.hit, self.endpoint, d)
