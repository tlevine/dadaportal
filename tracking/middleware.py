import re

from django.conf import settings

from .models import Hit
from .util import rand

class TrackingMiddleware:
    def process_request(self, request):
        'Generate the hit identifier.'
        for pattern in settings.DO_NOT_TRACK:
            if re.match(pattern, request.path_info):
                request.hit_id = None
                break
        else:
            request.hit_id = rand()

    def process_response(self, request, response):
        'Get the status code.'
        if request.hit_id != None:
            Hit.objects.filter(hit = request.hit_id).update(status_code = response.status_code)
        return response
