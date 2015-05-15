from lxml.html.clean import clean_html
from lxml.html import fromstring, tostring

TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'pre', 'img', 'table', 'blockquote',
        'ol', 'ul', 'dl', 'ul', }

def guess_slides(body):
    '''
    Wrap slides around top-level elements.
    '''
    return _subslides(fromstring(body))

def _subslides(element):
    result = b''
    if element.tag in TAGS:
        result += b'<div>' + tostring(element).strip() + b'</div>'
    elif element.tag == 'div':
        for subelement in element.getchildren():
            result += _subslides(subelement)
    return result
