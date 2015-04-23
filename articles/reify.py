import os, re, io
import datetime
import yaml, markdown, docutils.examples
from logging import getLogger

import lxml.html, lxml.etree

from django.conf import settings

logger = getLogger(__name__)

def parse(filename):
    formatter = FORMATS[re.match(EXTENSION, filename).group(1)]
    with open(filename) as body_fp:
        head_fp = io.StringIO()
        for line in body_fp:
            if re.match(r'^-+\s+$', line):
                # Dashed line
                head_fp.seek(0)
                break
            elif re.match(r'^\s*$', line):
                # Empty line before a dashed line
                head_fp.truncate(0)
                body_fp.seek(0)
                break
            else:
                head_fp.write(line)
        else:
            # If there was no dashed line,
            head_fp.truncate(0)
            body_fp.seek(0)
        try:
            head = yaml.load(head_fp)
        except yaml.scanner.ScannerError:
            logger.warning('Invalid YAML header at %s' % filename)
            head = {}
        body = formatter(body_fp)
        if type(head) != dict:
            head = {}
    return head, body

def rst(fp):
    return docutils.examples.html_body(fp.read(), doctitle = False)

def md(fp):
    return markdown.markdown(fp.read())

def md_plus(fp):
    parser = markdown.Markdown(extensions = ['markdown.extensions.tables'])
    return parser.convert(fp.read())

def read(fp):
    return fp.read()

FORMATS = {
    'mdwn': md,
    'md': md,
    'mdwn+': md_plus,
    'md+': md_plus,
    'rst': rst,
    'txt': read,
    'html': read,
}
EXTENSION = re.compile(r'^.*\.([a-z+]+)$')

def reify(filename):
    endpoint = os.path.dirname(filename)
    path = os.path.join(settings.ARTICLES_DIR, filename)
    dn, fn = os.path.split(path)
    if not fn.startswith('index.'):
        return

    m = re.match(EXTENSION, fn)
    if not (m and m.group(1) in FORMATS):
        return

    head, body = parse(path)
    try:
        html = lxml.html.fromstring(body)
    except lxml.etree.XMLSyntaxError:
        logging.warn('Invalid XML at %s' % path)
    else:
        for key, tag in [('title', 'h1'), ('description', 'p')]:
            if key not in head:
                tags = html.xpath('//' + tag)
                if len(tags) > 0:
                    head[key] = tags[0].text_content()
                else:
                    head[key] = ''

        srcs = html.xpath('//img/@src')
        if len(srcs) > 0:
            for service in ['twitter', 'facebook']:
                key = '%s_image' % service
                if key not in head:
                    head[key] = urljoin(endpoint, srcs[0])

    for field in ['title', 'description']:
        for service in ['facebook', 'twitter']:
            key = '%s_%s' % (service, field)
            if key not in head:
                head[key] = head[field]

    data = {
        'endpoint': endpoint,
        'body': body,
    }
    for key in data:
        if key in head:
            tpl = 'Key "%s" is reserved; you can\'t use it in an article header.'
            raise ValueError(tpl % key)
    data.update(head)
    return data
