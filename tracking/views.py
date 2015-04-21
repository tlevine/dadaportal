import logging, datetime

from django.shortcuts import render
from django.http import HttpResponse

from .models import Hit

logger = logging.getLogger(__name__)

def _get_hit_id(method, request):
    if 'hit_id' not in getattr(request, method):
        return None

    hit_id_raw = getattr(request, method)['hit_id']
    try:
        hit_id = int(hit_id_raw)
    except ValueError:
        return None

    try:
        hit = Hit.objects.get(hit = hit_id)
    except Hit.DoesNotExist:
        logger.warn('Hit "%d" was missing.' % hit_id)
        return None
    else:
        return hit

def followup_ico(request):
    hit = _get_hit_id('GET', request)
    if hit == None:
        return HttpResponse(status = 403)

    hit.javascript_enabled = False
    hit.save()
    return HttpResponse(content_type = 'image/x-icon',
        content = b'\x00\x00\x01\x00\x01\x00\x01\x01\x02\x00\x01\x00\x01\x008\x00\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa1W\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def followup_js(request):
    '''
    Finish the tracking after the XHR.
    '''
    hit = _get_hit_id('POST', request)
    if hit == None:
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
    hit.javascript_enabled = True
    hit.save()
    return render(request, 'tracking-track.txt')


def overview(request):
    return render(request, 'tracking-overview.html')
