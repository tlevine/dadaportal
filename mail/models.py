'''
http://www.jwz.org/doc/threading.html
'''
import email, os

from lxml.html.clean import clean_html

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
    is_mailing_list = m.BooleanField(null = False, default = False)

    @staticmethod
    def discover():
        for dirpath, dirnames, filenames in os.walk(settings.MAIL_DIR):
            for filename in filenames:
                yield os.path.join(dirpath, filename)

    @staticmethod
    def reify(filename):
        with open(filename) as fp:
            m = email.message_from_file(fp)

        date = m.get('date')
        if date != None:
            date = email.utils.parsedate_to_datetime(date)

        return {
            'is_mailing_list': len([k for k in m.keys() if k.lower().startswith('list')]),
            'datetime': date,
            '_from': m.get('from', ''),
            'to': m.get('to', ''),
            'cc': m.get('cc', ''),
            'subject': m.get('subject', ''),
            'body': _body(m),
        }

    def __str__(self):
        msg = '%(class)s "%(instance)s"'
        params = {
            'class': self.__class__.__name__,
            'instance': self.subject,
        }
        return msg % params

def _body(message):
    body = message.get_payload()
    if 'html' in message.get_content_type().lower():
        body = clean_html(body)
    return body
