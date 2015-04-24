import datetime

from ..models import (
    _parse_message_id, _decode_header,
    Message,
)

def test_parse_message_id_none():
    'If the message-id is None, result should also be None.'
    assert None == _parse_message_id(None)

def test_parse_message_id_weird():
    'If the message-id is weird, result should also be None.'
    assert None == _parse_message_id('aoestu astoehusa toehusanoehus naoehu >>> s<<< !!')

def test_parse_message_id_none():
    'If the message-id is standard, result should be appropriate'
    assert _parse_message_id('<abc@def>') == 'abc@def'

def test_decode_header():
    observed = _decode_header('Mez-Kanada =?UTF-8?B?UmVua29udGnEnW8gZW4gVG9yb250bw==?=')
    assert observed == 'Mez-Kanada Renkontiĝo en Toronto'
     
def test_parts():
    'Parts should be a list of names.'
    m = Message(
        message_id = 'abc@def.g',

        datetime = datetime.datetime.now(),
        subject = 'sub',
        _from = 'fr',
        to = 'to',
        cc = 'cc',

        body = 'body',

        partsjson = '[null, "garzweiler.png"]',
       #thread_id = m.Column(s.String)
        is_mailing_list = True,
    )
    assert m.parts == [None, 'garzweiler.png']
