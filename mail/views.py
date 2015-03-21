from django.shortcuts import render

# Template is 'mail-thread'
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

    return {
        'q': querystr,
        'title': title,
        'parts': parts,
        'body': body,
        'threads': list(hierarchy(query)),
    }

def attachment(request, querystr, n):
    db = Database()
    query = Query(db, '(not from:%s) and %s' % (ARTICLE_NOTMUCH_FROM, querystr))
    if query.count_messages() != 1:
        redirect('/@/%s/' % querystr)
    else:
        message = next(iter(query.search_messages()))
        parts = message.get_message_parts()
        i = n - 1
        if i >= len(parts):
            abort(404)
        else:
            part = parts[i]
            content_type = part.get_content_type()
            response.content_type = content_type

            fn = part.get_filename()
            if fn != None:
                response.headers['content-disposition'] = 'filename="%s";' % unidecode(fn).replace('"', '')

            payload = message.get_part(n)
            if 'html' in content_type.lower():
                return clean_html(payload)
            else:
                return payload

# @app.get('/@/<querystr:path>')
def search_redir(querystr):
    'Must come after all the other mail routes'
    redirect('/@/%s/' % querystr)
