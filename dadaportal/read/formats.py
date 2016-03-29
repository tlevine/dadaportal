import os, re, io, json
from urllib.parse import urljoin
import datetime
import yaml, markdown, docutils.examples
from logging import getLogger

import lxml.html, lxml.etree

logger = getLogger(__name__)

def rst(fp):
    return docutils.examples.html_body(fp.read(), doctitle = False)

def md(fp):
    return markdown.markdown(fp.read())

def md_plus(fp):
    parser = markdown.Markdown(extensions = ['markdown.extensions.tables'])
    return parser.convert(fp.read())

def read(fp):
    return fp.read()

formats = {
    'mdwn': md,
    'md': md,
    'mdwn+': md_plus,
    'md+': md_plus,
    'rst': rst,
    'txt': read,
    'html': read,
}
