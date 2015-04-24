import re
from urllib.parse import urlencode
from email import message_from_binary_file

from unidecode import unidecode

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Message
from .util import encode_charset, decode_charset

def index(request):
    messages = [{'message_id': a.message_id, 'subject': a.subject} \
        for a in Message.objects.all()]
    return render(request, 'mail/index.html', {'messages': messages})

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
        'from': _redact(m.ffrom),
        'to': _redact(m.to),
        'cc': _redact(m.cc),
        'body': m.body,

        'parts': m.parts,
        # Add thread eventually
    }
    return render(request, 'mail/message.html', params)

def attachment(request, message_id, i):
    i = int(i)
    try:
        message_db = Message.objects.get(message_id = message_id)
    except Message.DoesNotExist:
        raise Http404('Message is not cached in the database or doesn\'t exist at all.')

    with open(message_db.filename, 'rb') as fp:
        message_file = message_from_binary_file(fp)

    if message_file.is_multipart():
        parts = message_file.get_payload()
    else:
        parts = [message_file]

    if i >= len(parts):
        return HttpResponseRedirect('/@/%s/' % message_id)
    part = parts[i]

    # Things related to content type
    payload = part.get_payload(decode = True)
    content_type = part.get_content_type()

    # Start constructing the response
    for charset in part.get_charsets():
        try:
            payload.decode(charset)
        except UnicodeDecodeError:
            pass
        else:
            content_type = '%s; charset=%s' % (content_type, charset)
            break

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
        args = (message_db.message_id, i)
        content_disposition_right = 'filename="%s-part-%d.txt";' % args
    else:
        content_disposition_right = 'filename="%s";' % unidecode(fn).replace('"', '')

    response = HttpResponse(content = payload, content_type = content_type)
    response['content-disposition'] = content_disposition_left + content_disposition_right
    return response

def _redact(address):
    return re.sub(r'@[^, >]+', '@...', address)
