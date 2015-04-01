import logging, datetime

from django.shortcuts import render
from django.http import HttpResponse

from .models import Hit

logger = logging.getLogger(__name__)

def track_xhr(request):
    '''
    Finish the tracking after the XHR.
    '''
    if 'hit_id' not in request.POST:
        return HttpResponse(status = 403)
    hit_id = request.POST['hit_id']
    try:
        hit = Hit.objects.get(hit = hit_id)
    except Hit.DoesNotExist:
        logger.warn('Hit "%d" was missing.' % hit_id)
        return HttpResponse(status = 403)

    # Save values from the highest scroll.
    dimensions = [('scrollMaxX', 'pageXOffset', 'availWidth'),
                  ('scrollMaxY', 'pageYOffset', 'availHeight')]
    for dimension in dimensions:
        old_scroll = getattr(hit, dimension[0])
        new_scroll = request.POST.get(dimension[0])
        if new_scroll == None:
            pass
        elif old_scroll == None or int(new_scroll) > old_scroll:
            for field in dimension:
                setattr(hit, field, request.POST.get(field))

    hit.datetime_end = datetime.datetime.now()
    hit.save()
    return render(request, 'track.txt')
