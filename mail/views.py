from notmuch import Database, Query
from unidecode import unidecode
from lxml.html.clean import clean_html

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .queries import hierarchy, subhierarchy

def search(request, querystr):
    db = Database()
    query = Query(db, querystr)

    if query.count_messages() == 1:
        message = next(iter(query.search_messages()))
        title = message.get_header('subject')
        try:
            parts = [(i + 1, part.get_filename('No description')) \
                     for i, part in enumerate(message.get_message_parts())]
            body = message.get_part(1)
        except UnicodeDecodeError:
            parts = []
            body = 'There was an encoding problem with this message.'
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
    return render(request, 'mail-thread.html', params)

def attachment(request, querystr, n):
    db = Database()
    query = Query(db, '(not from:%s) and %s' % (ARTICLE_NOTMUCH_FROM, querystr))

    if query.count_messages() != 1:
        return HttpResponseRedirect('/@/%s/' % querystr)

    message = next(iter(query.search_messages()))
    parts = message.get_message_parts()
    i = int(n) - 1
    if i >= len(parts):
        return HttpResponseRedirect('/@/%s/' % querystr)

    part = parts[i]

    # Things related to content type
    content_type = part.get_content_type()
    payload = message.get_part(n)
    if 'html' in content_type.lower():
        payload = clean_html(payload)

    # Start constructing the response
    response = HttpResponse(content = payload, mimetype = content_type)

    # Content disposition
    fn = part.get_filename()
    if fn != None:
        response['content-disposition'] = 'filename="%s";' % unidecode(fn).replace('"', '')

    return response

# @app.get('/@/<querystr:path>')
def search_redir(querystr):
    'Must come after all the other mail routes'
    return HttpResponseRedirect('/@/%s/' % querystr)
