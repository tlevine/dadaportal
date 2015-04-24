from ..util import decode_header

def test_decode_header():
    observed = decode_header('Mez-Kanada =?UTF-8?B?UmVua29udGnEnW8gZW4gVG9yb250bw==?=')
    assert observed == 'Mez-Kanada Renkontiĝo en Toronto'
