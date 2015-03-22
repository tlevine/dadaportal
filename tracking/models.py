import datetime

from django.db import models

class Hit(models.Model):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'

    # Populated on the first request
    hit = models.BigIntegerField(primary_key = True)
    session = models.BigIntegerField(null = False, blank = False)
    datetime_start = models.DateTimeField(null = False, default = datetime.datetime.now)
    endpoint = models.TextField(null = False, blank = False)
    ip_address = models.IPAddressField(null = False, blank = False)
    user_agent = models.TextField(null = False)
    referrer = models.URLField(null = False)

    # Populated on the subsequent XHR, updated every few seconds
    datetime_end = models.DateTimeField(null = True)
    availWidth = models.IntegerField(null = True)
    availHeight = models.IntegerField(null = True)
    scrollMaxX = models.IntegerField(null = True)
    scrollMaxY = models.IntegerField(null = True)
    pageXOffset = models.IntegerField(null = True)
    pageYOffset = models.IntegerField(null = True)

    def __str__(self):
        return str(self.hit)
