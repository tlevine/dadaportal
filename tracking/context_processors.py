from .models import Hit
from .util import rand

def tracking(request):
    '''
    Begin the tracking on the fundamental (probably HTML) page load.

    The hit_id should be rendered in the template so it can be passed
    along in the XHR.
    '''
    if 'session_id' not in request.session:
        request.session['session_id'] = rand()
    Hit.objects.create(hit = request.hit_id,
                       session = request.session['session_id'],
                       ip_address = request.META['REMOTE_ADDR'],
                       user_agent = request.META['HTTP_USER_AGENT'],
                       referrer = request.META.get('HTTP_REFERER', ''))
    return {'hit_id': request.hit_id}
