import lxml.etree

_utf8parser = lxml.etree.HTMLParser(encoding='utf-8')
def fromutf8(x):
    body = lxml.etree.HTML(x, parser=_utf8parser).xpath('./body')[0]
    body.tag = 'div'
    return body
