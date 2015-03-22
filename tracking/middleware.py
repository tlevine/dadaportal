from random import getrandbits

from .models import Hit

def rand():
    return getrandbits(62)

class TrackingMiddleware:
    '''
    Begin the tracking on the fundamental (probably HTML) page load.

    The hit_id should be rendered in the template so it can be passed
    along in the XHR.
    '''
    def process_response(self, request, response):
        if 'session_id' not in request.session:
            request.session['session_id'] = rand()
        hit_id = rand()
        Hit.objects.create(hit = hit_id,
                           session = request.session['session_id'],
                           ip_address = request.META['REMOTE_ADDR'],
                           user_agent = request.META['HTTP_USER_AGENT'],
                           referrer = request.META.get('HTTP_REFERER', ''))
        print(hit_id)
        if hasattr(response, 'context_data'):
            print(response.context_data)
            response.context_data['hit_id'] = self.hit_id
  #     response.context_data['hit_id'] = self.hit_id
        return response

