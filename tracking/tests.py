from django.test import Client, RequestFactory

from ..models import Hit
from ..context_processors import tracking

def test_tracking():
    Hit.objects.all().delete()
    c = Client()
    response = c.get('/')

    hit = next(Hit.objects.all())
    assert str(hit.session) in response.content
