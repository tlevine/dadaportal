import logging, datetime

from .models import Hit, Search

logger = logging.getLogger(__name__)

def track_nonsearch(request):
    '''
    Begin the tracking on the fundamental (probably HTML) page load.

    The hit_id should be rendered in the template so it can be passed
    along in the XHR.
    '''
    if 'session_id' not in request.session:
        request.session['session_id'] = random.getrandbits(128)
    hit_id = random.getrandbits(128)

    hit = Hit.objects.create(hit = hit_id,
                             session = request.session['session_id'],
                             ip_address = request.META.REMOTE_ADDR,
                             user_agent = request.META.HTTP_USER_AGENT,
                             referrer = request.META.HTTP_REFERER)

    return hit_id

def track_search(request, search_terms:str, email_only:bool, n_results:int):
    hit_id = track_nonsearch(request)
    Search.objects.create(hit = hit_id, terms = search_terms,
                          email_only = email_only, n_results = n_results)
    return hit_id


XHR_FIELDS = [
    'screen_width', 'screen_height',
]
def track_xhr(request):
    '''
    Finish the tracking after the XHR.
    '''
    try:
        hit = Hit.objects.get(hit = request.session['hit_id'])
    except Hit.DoesNotExist:
        logger.warn('Session "%d" was missing.' % request.session['session_id'])
        return

    for field in XHR_FIELDS:
        setattr(hit, field, request.POST.get(field))
    hit.datetime_end = datetime.datetime.now()
    hit.save()
