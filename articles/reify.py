import os, re, io, json
from urllib.parse import urljoin
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
    endpoint = os.path.relpath(os.path.dirname(filename), settings.ARTICLES_DIR)
    path = os.path.join(settings.ARTICLES_DIR, filename)
    dn, fn = os.path.split(path)
    if not fn.startswith('index.'):
        return

    m = re.match(EXTENSION, fn)
    if not (m and m.group(1) in FORMATS):
        return

    head, body = parse(path)
    data = {
        'endpoint': endpoint,
        'body': body,
    }
    data['tagsjson'] = json.dumps(head.get('tags', []))

    try:
        html = lxml.html.fromstring(body)
    except lxml.etree.XMLSyntaxError:
        logger.debug('%s is not XML (It might be text.)' % path)
    else:
        for key, tag in [('title', 'h1'), ('description', 'p')]:
            if key in head:
                data[key] = head[key]
            else:
                tags = html.xpath('//' + tag)
                if len(tags) > 0:
                    data[key] = tags[0].text_content()

        srcs = html.xpath('//img/@src')
        if len(srcs) > 0:
            for service in ['twitter', 'facebook']:
                key = '%s_image' % service
                if key not in head:
                    data[key] = urljoin(endpoint, srcs[0])

        data['body'] = lxml.html.tostring(link_headers(link_img(html)))

    data['secret'] = head.get('secret', False)
    for key in ['redirect', 'title']:
        if key in head:
            data[key] = head[key]

    if ('title' not in data or not data['title']) and '/' not in endpoint:
        data['title'] = endpoint.replace('-', ' ')

    for field in ['title', 'description']:
        for service in ['facebook', 'twitter']:
            key = '%s_%s' % (service, field)
            if key in head:
                data[key] = head[key]
            elif field in head:
                data[key] = head[field]
            elif field in data:
                data[key] = data[field]

    return data

def link_img(html):
    for img in html.xpath('//img[not(../self::a)]'):
        a = lxml.html.Element('a', href = img.xpath('@src')[0])
        parent = img.getparent()
        parent.replace(img, a)
        a.append(img)
    return html

def link_headers(html):
    x = '//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]'
    for h in html.xpath(x):
        if 'id' not in h.attrib:
            h.attrib['id'] = h.text.lower().replace(' ', '-')
        a = lxml.html.Element('a', href = '#' + h.attrib['id'])
        parent = h.getparent()
        parent.replace(h, a)
        a.append(h)
    return html
