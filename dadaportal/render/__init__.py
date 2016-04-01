import os
import datetime

import lxml.html

from jinja2 import FileSystemLoader, Environment
from . import html_utils, big_utils

TEMPLATE_DIR = os.path.abspath(os.path.join(__file__, '..', 'templates'))
ENV = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

def html(title, description, body, include_footer):
    tpl = ENV.get_template('article.html')

    x = lxml.html.fromstring(body.encode('latin1'))
    y = html_utils.link_img(html_utils.link_headers(x))
    body = lxml.html.tostring(y, encoding='utf-8').decode('utf-8')

    now = datetime.datetime.now()

    return tpl.render(title=title, description=description, body=body,
                      include_footer=include_footer,
                      modified=now.strftime('%Y-%m-%d %H:%M UTC'),
                      modified_c=now.ctime())

def slides(title, description, body):
    tpl = ENV.get_template('slides.html')

    x = lxml.html.fromstring(body.encode('utf-8'))
    body = big_utils.subslides(x).decode('utf-8')

    return tpl.render(title=title, description=description, body=body)

renderers = {
    'html': html,
    'slides': slides,
}
