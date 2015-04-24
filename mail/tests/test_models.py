from ..models import _parse_message_id

def test_parse_message_id_none():
    'If the message-id is None, result should also be None.'
    assert None == _parse_message_id(None)

def test_parse_message_id_weird():
    'If the message-id is weird, result should also be None.'
    assert None == _parse_message_id('aoestu astoehusa toehusanoehus naoehu >>> s<<< !!')

def test_parse_message_id_none():
    'If the message-id is standard, result should be appropriate'
    assert _parse_message_id('<abc@def>') == 'abc@def'
