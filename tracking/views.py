import logging, datetime

from django.http import HttpResponse
from django.template.context_processors import csrf

from .models import Hit

logger = logging.getLogger(__name__)

def track_xhr(request):
    '''
    Finish the tracking after the XHR.
    '''
    print(8)
    if 'hit_id' not in request.POST:
        return HttpResponse(status = 403)
    hit_id = request.POST['hit_id']
    try:
        hit = Hit.objects.get(hit = hit_id)
    except Hit.DoesNotExist:
        logger.warn('Hit "%d" was missing.' % hit_id)
        return HttpResponse(status = 403)

    print(8)
    print(csrf(request))
    for field in ['availWidth', 'availHeight']:
        setattr(hit, field, request.POST.get(field))
    for field in ['scrollMaxX', 'scrollMaxY', 'pageXOffset', 'pageYOffset']:
        old = request.POST.get(field)
        new = getattr(hit, field)
        if old == None:
            setattr(hit, field, new)
        elif new == None:
            pass
        else:
            setattr(hit, field, max(old, new))

    hit.datetime_end = datetime.datetime.now()
    hit.save()
    print(csrf(request))
   #return HttpResponse(csrf(request))
