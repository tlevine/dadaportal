import os

from ..reify import from_file, from_db, parse

def test_from_file(tmpdir):
    fn = os.path.join('article-name', 'index.txt')
    fp = tmpdir.mkdir('article-name').join('index.txt')
    fp.write('parameter: 8230\n------\nI am a banana.\n')
    head, body, meta = from_file(os.path.dirname(fp.strpath))
    assert head == {'parameter': 8230}
    assert body == 'I am a banana.\n'
    assert meta == {
        'description': 'I am a banana.',
        'facebook_description': 'I am a banana.',
        'twitter_description': 'I am a banana.',
        'modified': os.stat(fp.strpath).st_mtime,
        'filename': 'index.txt',
        'redirect': None,
    }

def test_1_parse():
    head, body = parse(os.path.join('articles', 'tests', 'fixtures', '1.rst'))
    assert head == {}
    assert '<h1>Heading 1</h1>' in body
    assert '<p>Paragraph</p>' in body
    assert '<h2>Heading 2, a</h2>' in body
    assert '<h2>Heading 2, b</h2>' in body
