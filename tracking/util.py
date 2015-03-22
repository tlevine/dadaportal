from random import getrandbits

from django.conf import settings

def rand():
    return getrandbits(settings.HIT_ID_SIZE)

