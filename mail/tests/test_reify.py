import os
from email import message_from_file

from ..models import _body

def _fixture(fn):
    return os.path.join(os.path.dirname(__file__), 'fixtures', fn)

def test_body():
    'Body should be parsed correctly.'
    fn = '/home/tlevine/public-cur-emails/1427975842_0.12340.calque,U=6,FMD5=3d067bedfe2f4677470dd6ccf64d05ed:2,S'
    with open(_fixture(fn)) as fp:
        m = message_from_file(fp)
    comment = 'Sérieux il rap ca mieux que certain Francais Bravoo.'
    assert comment in _body(m)

def test_bad_charset():
    'Body should be decoded properly, even if charset is not specified.'
    fn = '/home/tlevine/public-cur-emails/1428303348_2.10210.calque,U=7,FMD5=3d067bedfe2f4677470dd6ccf64d05ed:2,S'
    with open(_fixture(fn)) as fp:
        m = message_from_file(fp)
    comment = 'estas preta por akcepti aliĝojn kaj po'
    assert comment in _body(m)
