from django.conf import settings

def dadaportal(request):
    return {
        'site_title': settings.SITE_TITLE,
        'domain_name': settings.DOMAIN_NAME,
        'og_url': 'http://%s%s' % (settings.DOMAIN_NAME, request.path_info),
    }
