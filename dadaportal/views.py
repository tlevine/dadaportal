import os

import markdown

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render

def docs(request):
    with open(os.path.join(settings.BASE_DIR, 'requirements.txt')) as fp:
        requirements = [line.strip() for line in fp if not line.startswith('#')]
    params = {
        'requirements': requirements,
        'database': settings.DATABASES['default'],
    }
    variables = ['REMOTE_USER', 'DOMAIN_NAME', 'EMAIL_ADDRESS',
                 'REMOTE_SSH_HOST', 'REMOTE_MAIL_DIR',
                 'REMOTE_STATIC_ROOT', 'REMOTE_BASE_DIR', 'STATIC_URL']
    for var in variables:
        params[var] = getattr(settings, var)
    doc = get_template('dadaportal/install.md').render(Context(params))
    return render(request, 'dadaportal/docs.html', {'doc': markdown.markdown(doc)})

def infinite_redirect(request):
    'To annoy script kiddies'
    return HttpResponseRedirect(request.path_info)
