from .models import Hit
from .util import rand

def tracking(request):
    '''
    Begin the tracking on the fundamental (probably HTML) page load.

    The hit_id should be rendered in the template so it can be passed
    along in the XHR.
    '''
    if request.hit_id == None:
        d = {}

    else:
        if 'session_id' not in request.session:
            request.session['session_id'] = rand()

        Hit.objects.create(hit = request.hit_id,
                           session = request.session['session_id'],
                           endpoint = request.path_info,
                           querystring = request.META['QUERY_STRING'],
                           ip_address = request.META['REMOTE_ADDR'],
                           accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
                           user_agent = request.META.get('HTTP_USER_AGENT', ''),
                           referrer = request.META.get('HTTP_REFERER', ''))
        d = {'hit_id': request.hit_id}

    return d
