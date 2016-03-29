import pytest
from django.test import Client, override_settings

from ..views import _redact
from ..models import Message

#@pytest.mark.django_db
#def test_index():
#    'GET /mail/ should return a list of mails.'
#    Message.objects.create(

@pytest.mark.django_db
def test_redirect():
    'The legacy id: urls should be redirected.'
    c = Client()
    response = c.get('/@/id:abc/')
    assert 400 > response.status_code >= 300

def test_redact_named_email_address():
    assert _redact('Thomas Levine <blah@thomaslevine.com>') == 'Thomas Levine <[redacted]@[redacted]>'

def test_redact_plain_email_address():
    assert _redact('  blah@thomaslevine.com   ') == '  [redacted]@[redacted]   '

def test_redact_twitter_username():
    assert _redact('Twitter: @thomaslevine ') == 'Twitter: @thomaslevine '

def test_redact_newline():
    original = '> > discuss@lists.something.org\n> > https://lists.something.org/mailman/listinfo/discuss'
    expected = '> > [redacted]@[redacted]\n> > https://lists.something.org/mailman/listinfo/discuss'
    assert _redact(original) == expected

def test_redact_garbled_email_link():
    original = '>someone@montrealgazette.com<mailto:someone@montrealgazette.com>  '
    expected = '>[redacted]@[redacted]<mailto:[redacted]@[redacted]>  '
    assert _redact(original) == expected
