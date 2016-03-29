import yaml
import os
import re
import logging

from . import header

INDEX = re.compile(r'^index\.([a-z0-9]+)$', flags=re.IGNORECASE)
logger = logging.getLogger(__name__)

def file(x):
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
        data = yaml.load(head_fp)
    except yaml.scanner.ScannerError:
        logger.warning('Invalid YAML dataer at %s' % filename)
        data = {}
    if type(data) != dict:
        data = {}

    formatter = [re.match(EXTENSION, filename).group(1)]
    data['body'] = formatter(body_fp) 
