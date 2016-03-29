import yaml
import json
import os
import re
import logging

from . import header, formats

INDEX = re.compile(r'^index\.([a-z0-9]+)$', flags=re.IGNORECASE)
logger = logging.getLogger(__name__)

FIELDS = {
    'title': str,
    'description': str,
    'body': str,
    'secret': bool,
}

def file(x):
    cachefile_basename = '.%s.cache' % os.path.basename(x)
    cachefile = os.path.join(os.path.dirname(x), cachefile_basename)

    if os.path.isfile(cachefile) and \
        os.stat(cachefile).st_mtime > os.stat(x).st_mtime:
        with open(cachefile) as fp:
            y = json.load(fp)
    else:
        y = file_nocache(x)

def file_nocache(x):
    if not os.path.isfile(x):
        raise TypeError('Not a file: %s' % x)

    bn = os.path.basename(x)
    m = re.match(INDEX, bn)
    if not m:
        return None

    m.group(1)

    with open(filename) as fp:
        head_fp, body_fp = header.split(fp)

    try:
        data.update(yaml.load(head_fp) or {})
    except yaml.scanner.ScannerError:
        logger.warning('Invalid YAML data at %s' % filename)
    data['body'] = formats.formats[extension](body_fp)
    
    if not set(data).issubset(FIELDS):
        raise ValueError('Bad fields: %s' % list(sorted(data)))
    for k, v in FIELDS.items():
        if not isinstance(data[k], v):
            raise ValueError('%s field has bad type: %s' % (k, v))

    return data
