import os
import re

INDEX = re.compile(r'^index\.([a-z0-9]+)$', flags=re.IGNORECASE)

def file(x):
    if not os.path.isfile(x):
        raise TypeError('Not a file: %s' % x)

    bn = os.path.basename(x)
    m = re.match(INDEX, bn)
    if not m:
        return None

    m.group(1)


    title = models.TextField(null = True)
    description = models.TextField(null = True)
    body = models.TextField(null = False)

    redirect = models.TextField(null = True)
    tagsjson = models.TextField(null = False) # JSON
    secret = models.BooleanField(null = False, default = False)
    tags
