import os
from email import message_from_file

from ..models import _body

def test_body():
    'Body should be parsed correctly.'
    fn = '/home/tlevine/public-cur-emails/1427975842_0.12340.calque,U=6,FMD5=3d067bedfe2f4677470dd6ccf64d05ed:2,S'
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', fn)) as fp:
        m = message_from_file(fp)
    comment = 'Sérieux il rap ca mieux que certain Francais Bravoo.'
    assert comment in _body(m)
