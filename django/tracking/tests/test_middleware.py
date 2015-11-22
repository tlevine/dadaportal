from django.test import Client, RequestFactory
import pytest

from ..models import Hit
from ..middleware import TrackingMiddleware

@pytest.mark.django_db
def test_process_trackable():
    'We should track a request to /!/'
    f = RequestFactory()
    request = f.get('/!/')
    
    t = TrackingMiddleware()
    t.process_request(request)
    assert isinstance(request.hit_id, int)
