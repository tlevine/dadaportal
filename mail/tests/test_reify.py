import os
from email import message_from_file

from ..models import _body

def _fixture(fn):
    return os.path.join(os.path.dirname(__file__), 'fixtures', fn)

def test_body():
    'Body should be parsed correctly.'
    with open(_fixture('youtube.eml')) as fp:
        m = message_from_file(fp)
    comment = 'Sérieux il rap ca mieux que certain Francais Bravoo.'
    assert comment in _body(m)

def test_bad_charset():
    'Body should be decoded properly, even if charset is not specified.'
    with open(_fixture('esperanto.yml')) as fp:
        m = message_from_file(fp)
    comment = 'estas preta por akcepti aliĝojn kaj po'
    assert comment in _body(m)
