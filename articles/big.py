from lxml.html.clean import clean_html
from lxml.html import fromstring, tostring

TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'pre', 'img', 'table',
        'ol', 'ul', 'dl', 'ul', }

def guess_slides(body):
    '''
    Wrap slides around top-level elements.
    '''
    tree = fromstring(body)
    if tree.tag == 'html':
        tree = tree[0]

    result = b''
    for element in tree:
        if element.tag in TAGS:
            result += b'<div>' + tostring(element).strip() + b'</div>'

    return result
