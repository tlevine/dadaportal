from django.conf import settings

def og_url(request):
    return {'og_url': 'http://%s/%s' % (settings.DOMAIN_NAME, request.path_info)}
