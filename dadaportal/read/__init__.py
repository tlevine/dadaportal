import yaml
import json
import os
import re
import logging
import io

from collections import ChainMap
from . import header, formats
from ..util import fromutf8

from jinja2 import FileSystemLoader, Environment

TEMPLATE_DIR = os.path.abspath(os.path.join(__file__, '..', 'templates'))
ENV = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

extensions = '|'.join(formats.formats)
INDEX = re.compile(r'^index\.(%s)$' % extensions, flags=re.IGNORECASE)
logger = logging.getLogger(__name__)

FIELDS = {
    'title': str,
    'description': str,
    'body': str,
    'publish': bool,
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
            explicit_data = yaml.load(head_fp)
        except yaml.scanner.ScannerError:
            logger.warning('Invalid YAML data at %s' % filename)
        if isinstance(explicit_data, dict):
            explicit_data.update(explicit_data)
        explicit_data['body'] = formats.formats[extension](body_fp)

    data = ChainMap(header.from_html(fromutf8(explicit_data['body'])),
                    expicit_data)
    
    if not set(data).issubset(FIELDS):
        logger.warn('Bad fields in %s' % filename)
    for k, v in FIELDS.items():
        if k in data and not isinstance(data[k], v):
            raise ValueError('%s field has bad type: %s' % (k, v))

    return data

def directory(x):
    tpl = ENV.get_template('directory.html')
    return {
        'title': os.path.basename(x),
        'description': '',
        'body': tpl.render(items = sorted(os.listdir(x))),
    }
