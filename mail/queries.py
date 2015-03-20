import datetime
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

def hierarchy(query):
    for i, thread in enumerate(query.search_threads()):
        yield [subhierarchy(message) for message in thread.get_toplevel_messages()]
        if i >= 100:
            # Stop after 100 threads
            break

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
    mailto = {
        'to': to,
        'subject': subject,
        'references': references,
        'in-reply-to': message.get_message_id(),
        'body': quote('''In reply to: http://mail.thomaslevine.com/!/id:%s/
''' % message.get_message_id())
    }
    if not to.endswith('@thomaslevine.com'):
        mailto['cc']: 'Thomas Levine <_@thomaslevine.com>'

    d = datetime.datetime.fromtimestamp(message.get_date())
    return {
        'message_id': message.get_message_id(),

        'weekday': d.strftime('%A'),
        'notmuchmonth': d.strftime('%Y-%m'),
        'month': d.strftime('%B'), 
        'notmuchday': d.strftime('%Y-%m-%d'),
        'day': d.strftime('%d'), 
        'notmuchyear': d.strftime('%Y'),
        'year': d.strftime('%Y'), 
        'time': d.strftime('%H:%M UTC'),

        'from': message.get_header('from'),
        'to': message.get_header('to'),
        'mailto': 'mailto:%(to)s?cc=%(cc)s&subject=%(subject)s&references=%(references)s&in-reply-to=%(in-reply-to)s&body=%(body)s' % mailto,
        'subject': message.get_header('subject'),
        'is_match': message.is_match(),
        'replies': [subhierarchy(reply) for reply in message.get_replies()]
    }

