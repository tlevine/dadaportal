import pytest
from django.test import Client, override_settings

from ..views import _redact

@pytest.mark.django_db
def test_redirect():
    'The legacy id: urls should be redirected.'
    c = Client()
    response = c.get('/@/id:abc/')
    assert 400 > response.status_code >= 300

def test_redact_named_email_address():
    assert _redact('Thomas Levine <blah@thomaslevine.com>') == 'Thomas Levine <blah@...>'

def test_redact_plain_email_address():
    assert _redact('  blah@thomaslevine.com   ') == '  blah@...   '

def test_redact_twitter_username():
    assert _redact('Twitter: @thomaslevine ') == 'Twitter: @thomaslevine '
