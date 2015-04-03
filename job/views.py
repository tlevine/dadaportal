from django.conf import settings
from django.shortcuts import render
from django.utils.translation import get_language_from_request

from .want import WANT, WANT_DEFAULT

def job(request):
    language = get_language_from_request(request)
    params = {
        'message': WANT.get(language, WANT_DEFAULT),
        'email_address': settings.EMAIL_ADDRESS,
    }
    return render(request, 'jobs.html', params)
