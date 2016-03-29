import datetime

from ..models import (
    _parse_message_id,
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
     
def test_parts():
    'Parts should be a list of names.'
    m = Message(
        message_id = 'abc@def.g',

        datetime = datetime.datetime.now(),
        subject = 'sub',
        ffrom = 'fr',
        to = 'to',
        cc = 'cc',

        body = 'body',

        partsjson = '[null, "garzweiler.png"]',
       #thread_id = m.Column(s.String)
        is_mailing_list = True,
    )
    assert m.parts == [None, 'garzweiler.png']
