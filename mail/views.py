import re

from notmuch import Database, Query as _Query
from unidecode import unidecode
from lxml.html.clean import clean_html

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .queries import hierarchy, subhierarchy


def Query(querystr):
    db = Database(settings.NOTMUCH_MAILDIR)
    return _Query(db, '(not from:%s) and %s' % (settings.NOTMUCH_SECRET, querystr))

def _magically_decode(bytestring):
    for encoding in ['utf-8', 'latin1']:
        try:
            return bytestring.decode('utf-8')
        except UnicodeDecodeError:
            pass

def search(request, querystr):
    query = Query(querystr)
    if query.count_messages() == 1:
        message = next(iter(query.search_messages()))
        title = message.get_header('subject')
        try:
            ps = message.get_message_parts()
            parts = [(i + 1, part.get_filename('No description')) \
                     for i, part in enumerate(ps)]
        except UnicodeDecodeError:
            parts = []
            body = 'There was an encoding problem with this message.'
        else:
            body = _magically_decode(message.get_part(1))
            if body == None:
                body = ps[0].get_payload()
    else:
        title = '"%s" emails' % querystr
        parts = []
        body = None

    params = {
        'q': querystr,
        'title': title,
        'parts': parts,
        'body': body,
        'threads': list(hierarchy(query)),
    }
    if body != None:
        params['message'] = params['threads'][0][0]
    return render(request, 'mail-thread.html', params)

def attachment(request, querystr, n):
    n = int(n)

    db = Database(settings.NOTMUCH_MAILDIR)
    query = Query(querystr)

    if query.count_messages() != 1:
        return HttpResponseRedirect('/@/%s/' % querystr)

    message = next(iter(query.search_messages()))
    parts = message.get_message_parts()
    i = n - 1
    if i >= len(parts):
        return HttpResponseRedirect('/@/%s/' % querystr)

    part = parts[i]

    # Things related to content type
    content_type = part.get_content_type()
    payload = message.get_part(n)
    if 'html' in content_type.lower():
        payload = clean_html(payload)

    # Start constructing the response
    response = HttpResponse(content = payload, content_type = content_type)

    # Content disposition
    fn = part.get_filename()

    # Force download on HTML if running it here could be unsafe.
    for ml in ['html', 'xml', 'svg']:
        if ml in content_type.lower():
            content_disposition_left = 'attachment; '
            break
    else:
        content_disposition_left = ''

    # Set the file name.
    if fn == None:
        args = (message.get_message_id(), n)
        content_disposition_right = 'filename="%s-part-%d.html";' % args
    else:
        content_disposition_right = 'filename="%s";' % unidecode(fn).replace('"', '')

    response['content-disposition'] = content_disposition_left + content_disposition_right
    return response

# @app.get('/@/<querystr:path>')
def search_redir(querystr):
    'Must come after all the other mail routes'
    return HttpResponseRedirect('/@/%s/' % querystr)
