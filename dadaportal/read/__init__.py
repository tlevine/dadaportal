import yaml
import json
import os
import re
import logging

from . import header, formats

extensions = '|'.join(formats.formats)
INDEX = re.compile(r'^index\.(%s)$' % extensions, flags=re.IGNORECASE)
logger = logging.getLogger(__name__)

FIELDS = {
    'title': str,
    'description': str,
    'body': str,
    'secret': bool,
}

def can_read(x):
    return re.match(INDEX, os.path.basename(x))

def file(filename):
    if not os.path.isfile(filename):
        raise TypeError('Not a file: %s' % filename)
    extension = can_read(filename).group(1)

    with open(filename) as fp:
        head_fp, body_fp = header.split(fp)
        try:
            data = yaml.load(head_fp)
        except yaml.scanner.ScannerError:
            logger.warning('Invalid YAML data at %s' % filename)
        if not isinstance(data, dict):
            data = {}
        data['body'] = formats.formats[extension](body_fp)
    
    if not set(data).issubset(FIELDS):
        logger.warn('Bad fields: %s' % list(sorted(data)))
    for k, v in FIELDS.items():
        if k in data and not isinstance(data[k], v):
            raise ValueError('%s field has bad type: %s' % (k, v))

    return data
