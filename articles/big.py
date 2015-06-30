from lxml.html.clean import clean_html
from lxml.html import fromstring, tostring

SLIDE_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'pre', 'img', 'table', 'blockquote',
              'video', 'iframe',
              'ol', 'ul', 'dl', 'ul', }

WRAPPER_TAGS = {'div', 'a', 'p'}

def guess_slides(body):
    '''
    Wrap slides around top-level elements.
    '''
    return _subslides(fromstring(body))

def _subslides(element):
    result = b''
    if element.tag in SLIDE_TAGS:
        # Add a space so images aren't backgrounds.
        result += b'<div>' + tostring(element).strip() + b'</div>'
    elif element.tag in WRAPPER_TAGS:
        for subelement in element.getchildren():
            result += _subslides(subelement)
    return result
