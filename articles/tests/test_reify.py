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
        'modified': os.stat(fp.strpath).st_mtime,
        'filename': 'index.txt',
        'redirect': None,
    }

def test_parse():
    parse(os.path.join('articles', 'tests', 'fixtures', '1.rst'))
