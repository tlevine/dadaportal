from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Message

def message_legacy(request, message_id):
    return HttpResponseRedirect('/@/%s/' % message_id)

def message(request, message_id):
    try:
        m = Message.objects.get(message_id = message_id)
    except Message.DoesNotExist:
        raise Http404('Message is not cached in the database or doesn\'t exist at all.')

    params = {
        'title': m.subject,
        'subject': m.subject,
        'datetime': m.datetime,
        'from': _redact(m._from),
        'to': _redact(m.to),
        'cc': _redact(m.cc),
        'body': m.body,

        'parts': parts,
        # Add thread eventually
    }
    return render(request, 'mail/message.html', params)

def attachment(request, message_id, part):
    i = int(part) - 1

    try:
        message_db = Message.objects.get(message_id = message_id)
    except Message.DoesNotExist:
        raise Http404('Message is not cached in the database or doesn\'t exist at all.')

    with open(message_db.filename) as fp:
        message_file = message_from_file(fp)

    if message.is_multipart():
        parts = message.get_payload()
    else:
        parts = [message]

    if i >= len(parts):
        return HttpResponseRedirect('/@/%s/' % message_id)
    part = parts[i]

    # Things related to content type
    payload = part.get_payload(decode = True)
    if 'html' in part.get_content_type().lower():
        payload = clean_html(payload)

    for charset in filter(None, m.get_charsets()):
        try:
            encoded_payload = payload.encode(charset)
        except UnicodeEncodeError:
            pass
        else:
            encoding = charset
            break
    else:
        encoded_payload = unidecode(payload).encode('utf-8')
        encoding = 'utf-8'

    # Start constructing the response
    response = HttpResponse(content = encoded_payload,
        content_type = content_type, encoding = encoding)

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
        content_disposition_right = 'filename="%s-part-%d.txt";' % args
    else:
        content_disposition_right = 'filename="%s";' % unidecode(fn).replace('"', '')
    response['content-disposition'] = content_disposition_left + content_disposition_right
    return response

def _redact(address):
    return re.sub(r'@[^, >]+', '@...', address)
