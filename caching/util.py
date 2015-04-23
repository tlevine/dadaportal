from django.conf import settings

def get(Class, endpoint):
    '''
    Get an object, using the cache if USE_CACHE is set and pretty
    much not using the cache if USE_CACHE is not set.
    '''
    obj = Class.objects.get(endpoint = endpoint)
    if not settings.USE_CACHE:
        obj.sync()
    return obj
