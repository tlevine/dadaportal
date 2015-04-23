from django.test import Client, RequestFactory
import pytest

from ..models import Hit
from ..context_processors import tracking

@pytest.mark.django_db
def test_tracking():
    'The hit_id should appear in the HTML.'
    Hit.objects.all().delete()
    c = Client()
    response = c.get('/')

    hit = next(Hit.objects.all())
    assert str(hit.session) in response.content

@pytest.mark.django_db
def test_yes_user_agent():
    'Tracking should work with a user agent.'
    f = RequestFactory(HTTP_USER_AGENT = 'Django/1.7')
    request = f.get('/')
    assert list(tracking(request).keys()) == ['hit_id']

@pytest.mark.django_db
def test_no_user_agent():
    f = RequestFactory()
    request = f.get('/')
    assert list(tracking(request).keys()) == ['hit_id']
