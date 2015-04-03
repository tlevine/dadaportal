import os, re, io
import yaml, markdown, docutils.examples
from logging import getLogger

import lxml.html, lxml.etree

from .models import ArticleCache

logger = getLogger(__name__)

def parse(filename):
    formatter = FORMATS[re.match(EXTENSION, filename).group(1)]
    with open(filename) as body_fp:
        head_fp = io.StringIO()
        for line in body_fp:
            if re.match(r'^-+\s$', line):
                head_fp.seek(0)
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
    return docutils.examples.html_body(fp.read())

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
def from_file(dirname):
    for just_fn in os.listdir(dirname):
        if just_fn.startswith('index.'):
            filename = os.path.join(dirname, just_fn)
            break
    else:
        return None, None, None
    m = re.match(EXTENSION, just_fn)
    if not (m and m.group(1) in FORMATS):
        return None, None, None

    head, body = parse(filename)
    if 'title' not in head:
        try:
            html = lxml.html.fromstring(body)
        except lxml.etree.XMLSyntaxError:
            pass
        else:
            h1s = html.xpath('//h1')
            if len(h1s) > 0:
                head['title'] = h1s[0].text_content()

    for field in ['title', 'description']:
        if field in head:
            for service in ['facebook', 'twitter']:
                service_field = '%s_%s' % (service, field)
                if service_field not in head:
                    head[service_field] = head[field]

    meta = {
        'modified': os.stat(filename).st_mtime,
        'filename': just_fn,
        'redirect': head.get('redirect'),
    }
    return head, body, meta

def from_db(article_cache):
    meta = {
        'modified': article_cache.modified,
        'filename': article_cache.filename,
        'endpoint': article_cache.endpoint,
    }
    return article_cache.head(), article_cache.body, meta
