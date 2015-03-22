import logging

from .models import Hit, Search, ArticleHitCounts

logger = logging.getLogger(__name__)

def track_nonsearch(request):
    '''
    Begin the tracking on the fundamental (probably HTML) page load.
    '''
    if 'session_id' not in request.session:
        request.session['session_id'] = random.getrandbits(128)
    session = request.session['session_id']
    hit = Hit.objects.create(session = session,
                             ip_address = request.META.REMOTE_ADDR,
                             user_agent = request.META.HTTP_USER_AGENT,
                             referrer = request.META.HTTP_REFERER)

def track_search(request, search_terms
    Search.objects.create(hit = hit.id, terms = search_terms,



XHR_FIELDS = [
    'screen_width', 'screen_height', 'seconds_on_page',
]
def track_xhr(request):
    '''
    Finish the tracking after the XHR.
    '''
    try:
        hit = Hit.objects.get(session = request.session['session_id'])
    except Hit.DoesNotExist:
        logger.warn('Session "%d" was missing.' % request.session['session_id'])
        return

    if not hit.fresh:
        hit.fresh = False
        hitcount = ArticleHitCounts.get_or_create(endpoint = hit.endpoint)
        hitcount.day_0 += 1
        hitcount.save()

    for field in XHR_FIELDS:
        setattr(hit, field, request.POST.get(field))

    hit.save()
