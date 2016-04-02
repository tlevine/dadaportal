import os
import datetime
import re

import lxml.html

from jinja2 import FileSystemLoader, Environment
from . import html_utils, big_utils
from ..util import fromutf8

TEMPLATE_DIR = os.path.abspath(os.path.join(__file__, '..', 'templates'))
ENV = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

def html(title, description, body, include_footer):
    tpl = ENV.get_template('article.html')

    x = fromutf8(body)
    y = html_utils.link_img(html_utils.link_headers(x))
    body = lxml.html.tostring(y, encoding='utf-8').decode('utf-8')

    now = datetime.datetime.now()

    return tpl.render(title=title, description=description, body=body,
                      include_footer=include_footer,
                      modified=now.strftime('%Y-%m-%d %H:%M UTC'),
                      modified_c=now.ctime())

def slides(title, description, body):
    tpl = ENV.get_template('slides.html')

    x = fromutf8(body.encode('utf-8'))
    body = big_utils.subslides(x).decode('utf-8')

    return tpl.render(title=title, description=description, body=body)

def image(i):
    height, width = i.size 
    if width*9/16 >= height:
        ratio = min(900/width, 1)
    else:
        ratio = min(500/height, 1)
    return i.resize(height*ratio, width*ratio)

def can_resize(fn):
    return re.match(r'.*(?:png|jpg|jpeg)$', fn)

renderers = {
    'html': html,
    'slides': slides,
}
