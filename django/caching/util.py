from django.conf import settings

def get(Class, **kwargs):
    '''
    Get an object, using the cache if USE_CACHE is set and pretty
    much not using the cache if USE_CACHE is not set.
    '''
    obj = Class.objects.get(**kwargs)
    if not settings.USE_CACHE:
        try:
            obj.sync()
        except FileNotFoundError:
            obj.delete()
            raise Class.DoesNotExist
    return obj
