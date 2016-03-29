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
