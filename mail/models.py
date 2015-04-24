'''
http://www.jwz.org/doc/threading.html
'''
import email, os, re, json

from django.conf import settings
from django.db import models as m
from django.core.urlresolvers import reverse

from caching import Cache

from .util import decode_charset, decode_header, clean_payload

class Message(Cache):
    message_id = m.TextField(blank = False, null = False, unique = True)

    datetime = m.DateTimeField(null = False)
    subject = m.TextField(null = False)
    ffrom = m.TextField(null = False)
    to = m.TextField(null = False)
    cc = m.TextField(null = False)

    body = m.TextField(null = False)

    partsjson = m.TextField(null = False)
    @property
    def parts(self):
        return json.loads(self.partsjson)
    @parts.setter
    def parts(self, value):
        self.partsjson = json.dumps(value)

   #thread_id = m.Column(s.String)
    is_mailing_list = m.BooleanField(null = False, default = False)

    def get_absolute_url(self):
        return reverse('mail/message', args = (self.message_id,))

    @staticmethod
    def discover():
        for dirpath, dirnames, filenames in os.walk(settings.MAIL_DIR):
            for filename in filenames:
                yield os.path.join(dirpath, filename)

    @staticmethod
    def reify(filename):
        with open(filename, 'rb') as fp:
            m = email.message_from_binary_file(fp)

        date = m.get('date')
        if date != None:
            date = email.utils.parsedate_to_datetime(date)

        return {
            'message_id': _parse_message_id(m.get('message-id')),
            'is_mailing_list': len([k for k in m.keys() if k.lower().startswith('list')]),
            'datetime': date,
            'ffrom': m.get('from', ''),
            'to': m.get('to', ''),
            'cc': m.get('cc', ''),
            'subject': decode_header(m.get('subject', '')),
            'body': clean_payload(m, decode_header(_body(m))),
            'partsjson': json.dumps(_parts(m)),
        }

    def __str__(self):
        msg = '%(class)s "%(instance)s"'
        params = {
            'class': self.__class__.__name__,
            'instance': self.subject,
        }
        return msg % params

def _body(message):
    if message.is_multipart():
        payload = message.get_payload()[0].get_payload(decode = True)
        try:
            body = decode_charset(message, payload)
        except ValueError:
            body = ''
    else:
        body = message.get_payload()
    return clean_payload(message, body)

def _parse_message_id(maybe_message_id):
    if maybe_message_id:
        m = re.match(r'^[^<]*<([^<]+)>.*$', maybe_message_id)
        if m:
            return m.group(1)

def _parts(m):
    if not m.is_multipart():
        return []
    unfiltered = enumerate(part.get_filename() for part in m.get_payload())
    return [(i, fn) for i, fn in unfiltered if fn]
