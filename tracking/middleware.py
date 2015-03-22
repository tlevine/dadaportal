from random import getrandbits

from .models import Hit, Search

class TrackingMiddleware:
    '''
    Begin the tracking on the fundamental (probably HTML) page load.

    The hit_id should be rendered in the template so it can be passed
    along in the XHR.
    '''
    def process_template_response(self, request, response):
        if 'session_id' not in request.session:
            request.session['session_id'] = getrandbits(128)
        hit_id = getrandbits(128)
        response.context_data['hit_id'] = hit_id
        Hit.objects.create(hit = hit_id,
                           session = request.session['session_id'],
                           ip_address = request.META['REMOTE_ADDR'],
                           user_agent = request.META['HTTP_USER_AGENT'],
                           referrer = request.META.get('HTTP_REFERER', ''))
        return response

def track_search(request, search_terms:str, email_only:bool, n_results:int):
    hit_id = track_nonsearch(request)
    Search.objects.create(hit = hit_id, terms = search_terms,
                          email_only = email_only, n_results = n_results)
    return hit_id
