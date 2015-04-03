import os

from .reify import reify

def test_reify(tmpdir):
    fn = os.path.join('article-name', 'index.txt')
    fp = tmpdir.mkdir('article-name').join('index.txt')
    fp.write('parameter: 8230\n------\nI am a banana.\n')
    head, body, meta = reify(os.path.dirname(fp.strpath))
    assert head == {'parameter': 8230}
    assert body == 'I am a banana.\n'
    assert meta == {
        'modified': os.stat(fp.strpath).st_mtime,
        'filename': 'index.txt',
        'redirect': None,
    }
