import os, re, io
import yaml, markdown, docutils.examples

import lxml.html, lxml.etree

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
        data = {
            'head': yaml.load(head_fp),
            'body': formatter(body_fp),
        }
        if type(data['head']) != dict:
            data['head'] = {}
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
def reify(article_dir, filename):
    m = re.match(EXTENSION, filename)
    if m and m.group(1) in FORMATS:
        data = parse(possibilities[0])
        try:
            html = lxml.html.fromstring(data['body'])
        except lxml.etree.XMLSyntaxError:
            pass
        else:
            h1s = html.xpath('//h1')
            if len(h1s) > 0 and 'title' not in data:
                data['title'] = h1s[0].text_content()
        if 'title' not in data:
            data['title'] = None
        return data
