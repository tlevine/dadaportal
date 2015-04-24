import pytest
from django.test import Client, override_settings

@pytest.mark.django_db
def test_redirect():
    'The legacy id: urls should be redirected.'
    c = Client()
    response = c.get('/@/id:abc/')
    assert 400 > response.status_code >= 300
