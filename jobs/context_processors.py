from django.utils.translation import get_language_from_request

from .want import WANT

def jobs(request):
    language = get_language_from_request(request)
    return {'request_job': language in WANT}
