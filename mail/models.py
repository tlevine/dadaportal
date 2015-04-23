'''
http://www.jwz.org/doc/threading.html
'''
from django.conf import settings
from django.db import models as m

from caching import Cache

class Message(Cache):
    message_id = m.TextField(blank = False, null = False, unique = True)

    datetime = m.DateTimeField(null = False)
    subject = m.TextField(null = False)
    _from = m.TextField(null = False)
    to = m.TextField(null = False)
    cc = m.TextField(null = False)

    body = m.TextField(null = False)

   #thread_id = m.Column(s.String)
    is_mailing_list = m.BooleanField(null = False)

    @staticmethod
    def discover():
        for dirpath, dirnames, filenames in os.walk(settings.MAIL_DIR):
            for filename in filenames:
                yield os.path.join(dirpath, filename)
