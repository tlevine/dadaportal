import os

import lxml.html

from ..reify import reify, parse, link_img

def test_1_parse():
    head, body = parse(os.path.join('articles', 'tests', 'fixtures', '1.rst'))
    assert head == {}
    assert '<h1>Heading 1</h1>' in body
    assert '<p>Paragraph</p>' in body
    assert '<h2>Heading 2, a</h2>' in body
    assert '<h2>Heading 2, b</h2>' in body

def test_img():
    html = lxml.html.parse(os.path.join('articles', 'tests', 'fixtures', 'img.html')).getroot()
    b = lxml.html.tostring(link_img(html)).replace(b'"', b'')
    assert b'<a href=a.png><img src=a.png' in b
    assert b'<a href=c.png>' in b
    assert b'<a href=b.png>' not in b
