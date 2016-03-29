import os

import lxml.html

from . import html_utils, big_utils

def html(title, description, body):
    x = lxml.html.fromstring(body.encode('utf-8'))
    y = html_utils.link_img(html_utils.link_headers(x))
    z = lxml.html.tostring(y)
    raise NotImplementedError('Apply template.')
