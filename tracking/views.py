import logging, datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Hit

logger = logging.getLogger(__name__)

XHR_FIELDS = [
    'screen_width', 'screen_height',
]
@csrf_exempt
def track_xhr(request):
    '''
    Finish the tracking after the XHR.
    '''
    if 'hit_id' not in request.POST:
        print(1)
        return HttpResponse(status = 403)
    hit_id = request.POST['hit_id']
    try:
        hit = Hit.objects.get(hit = hit_id)
    except Hit.DoesNotExist:
        print(2)
        logger.warn('Hit "%d" was missing.' % hit_id)
        return HttpResponse(status = 403)

    for field in XHR_FIELDS:
        setattr(hit, field, request.POST.get(field))
    hit.datetime_end = datetime.datetime.now()
    hit.save()
    print(3)
    return HttpResponse(status=204)
