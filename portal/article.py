import os, re, io
import yaml, markdown, docutils.examples

import lxml.html, lxml.etree

def get_possibilities(article_dir, endpoint):
    if os.path.isdir(os.path.join(article_dir, endpoint)):
        return get_possibilities(article_dir, os.path.join(endpoint, 'index'))
    partial_directory, identifier = os.path.split(endpoint)
    directory = os.path.join(article_dir, partial_directory)
    return [os.path.join(directory, x) for x in os.listdir(directory) \
            if _is_possible(x, identifier)]

SEPARATOR = re.compile(r'^-+$')

def parse(filename):
    formatter = FORMATS[re.match(EXTENSION, filename).group(1)]
    with open(filename) as body_fp:
        head_fp = io.StringIO()
        for line in head_fp:
            if re.match(SEPARATOR, line):
                head_fp.seek(0)
                break
            else:
                head_fp.write(line)
        else:
            # If there was no dashed line,
            head_fp.truncate(0)
            body_fp.seek(0)
        data = yaml.load(head_fp)
        if not type(data) == dict:
            data = {}
        data['body'] = formatter(body_fp)
    return data

def rst(fp):
    return docutils.examples.html_body(fp.read())

def md(fp):
    return markdown.markdown(fp.read())

def read(fp):
    return fp.read()

FORMATS = {
    'mdwn': md,
    'md': md,
    'rst': rst,
    'txt': read,
    'html': read,
}
EXTENSION = re.compile(r'^.*\.([a-z]+)$')

def _is_possible(x, identifier):
    if not x.startswith(identifier):
        return False
    m = re.match(EXTENSION, x)
    if not (m and m.group(1) in FORMATS):
        return False
    return True

def reify(article_dir, endpoint):
    possibilities = get_possibilities(article_dir, endpoint)
    if len(possibilities) == 1:
        m = re.match(EXTENSION, possibilities[0])
        if m and m.group(1) in FORMATS:
            data = parse(possibilities[0])
            data['endpoint'] = endpoint
            try:
                html = lxml.html.fromstring(data['body'])
            except lxml.etree.XMLSyntaxError:
                pass
            else:
                h1s = html.xpath('//h1')
                if len(h1s) > 0 and 'title' not in data:
                    data['title'] = h1s[0].text_content()
            return data
    elif len(possibilities) > 1:
        raise ValueError('Multiple possibilites:\n* ' + '* \n'.join(possibilities) + '\n')

def is_static(endpoint):
    m = re.match(EXTENSION, endpoint)
    return m and m.group(1) not in FORMATS
