from lxml.html.clean import clean_html
from lxml.html import fromstring, tostring, Element

SLIDE_TAGS = {'h2', 'h3', 'h4', 'h5', 'h6',
              'pre', 'img', 'table', 'blockquote',
              'iframe',
              'ol', 'ul', 'dl', 'ul', }

WRAPPER_TAGS = {'div', 'a', 'p'}

def subslides(element):
    result = b''

    if element.tag in SLIDE_TAGS:
        result += b'<div>' + tostring(element).strip() + b'</div>'

    elif element.tag == 'video' and 'src' in element.attrib:
        href = element.attrib['src']
        anchor = Element('a', href = href)
        anchor.text = element.attrib.get('title', href)
        result += b'<div>' + tostring(anchor).strip() + b'</div>'

    elif element.tag in WRAPPER_TAGS:
        for subelement in element.getchildren():
            result += subslides(subelement)

    #   if element.tag == 'p':
    #       result += ('<notes>' + element.text_content() + '</notes>').encode('utf-8')
    return result
