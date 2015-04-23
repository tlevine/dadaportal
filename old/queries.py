import re
import subprocess
import datetime
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from notmuch.message import NullPointerError

from django.conf import settings

def hierarchy(query):
    try:
        for i, thread in enumerate(query.search_threads()):
            if i >= settings.MAX_SEARCH_RESULTS:
                break
            yield [subhierarchy(message) for message in thread.get_toplevel_messages()]
    except NullPointerError:
        subprocess.Popen(['notmuch', 'new']).wait()
        # And just truncate the request silently.

def subhierarchy(message):
    '''
    Annoyingly, see the note on "unsafe headers" RFC 2368.
    http://tools.ietf.org/html/rfc2368
    '''
    to = message.get_header('reply-to')
    if to == '':
        to = message.get_header('from')

    subject = message.get_header('subject')
    if not subject.lower().startswith('re'):
        subject = 'RE: ' + subject

    references = message.get_header('references')
    if references != '':
        references = references + '\n'
    references = references + message.get_message_id()
    if settings.EMAIL_ADDRESS not in to:
        cc = '%s <%s>' % (settings.NAME, settings.EMAIL_ADDRESS)
    else:
        cc = ''
    mailto = {
        'to': to,
        'cc': cc,
        'subject': subject,
        'references': references,
        'in-reply-to': message.get_message_id(),
        'body': quote('''In reply to: http://%s/@/id:%s/
''' % (settings.DOMAIN_NAME, message.get_message_id()))
    }

    d = datetime.datetime.fromtimestamp(message.get_date())
    return {
        'message_id': message.get_message_id(),

        'notmuchdate': d.strftime('%Y-%m-%d'),
        'date': d.strftime('%A, %B %d, %Y'), 
        'time': d.strftime('%H:%M UTC'),

        'from': _redact(message.get_header('from')),
        'to': _redact(message.get_header('to')),
        'mailto': 'mailto:%(to)s?cc=%(cc)s&subject=%(subject)s&references=%(references)s&in-reply-to=%(in-reply-to)s&body=%(body)s' % mailto,
        'subject': message.get_header('subject'),
        'is_match': message.is_match(),
        'replies': [subhierarchy(reply) for reply in message.get_replies()]
    }


def _redact(address):
    return re.sub(r'@[^, >]+', '@...', address)
