from lxml.html.clean import clean_html
from lxml.html import fromstring, tostring

TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'pre', 'img', 'table',
        'ol', 'ul', 'dl', 'ul', }

def guess_slides(body):
    '''
    Wrap slides around top-level elements.
    '''
    html = fromstring(body)
    result = b''

    for element in html:
        if element.tag in TAGS:
            result += b'<div>' + tostring(element).strip() + b'</div>'
        else:
            result += tostring(element)

    return result
