import lxml.etree

_utf8parser = lxml.etree.HTMLParser(encoding='utf-8')
def fromutf8(x):
    return lxml.etree.HTML(x, parser=_utf8parser)
