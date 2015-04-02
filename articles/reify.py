import os, re, io
import yaml, markdown, docutils.examples
from logging import getLogger

import lxml.html, lxml.etree

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
def reify(article_dir, filename):
    m = re.match(EXTENSION, filename)
    if not (m and m.group(1) in FORMATS):
        return None, None

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

    return head, body
