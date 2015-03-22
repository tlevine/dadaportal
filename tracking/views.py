import logging, datetime

from .models import Hit

logger = logging.getLogger(__name__)

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
        logger.warn('Hit "%d" was missing.' % request.session['hit_id'])
        return HttpResponse(status = 403)

    for field in XHR_FIELDS:
        setattr(hit, field, request.POST.get(field))
    hit.datetime_end = datetime.datetime.now()
    hit.save()
    return HttpResponse(status=204)
