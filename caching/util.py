from django.conf import settings

def get(Class, pk):
    '''
    Get an object, using the cache if USE_CACHE is set and pretty
    much not using the cache if USE_CACHE is not set.
    '''
    obj = Class.objects.get(pk = pk)
    if not settings.USE_CACHE:
        obj.sync()
    return obj
