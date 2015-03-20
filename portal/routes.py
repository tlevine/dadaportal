import os
from functools import partial

from unidecode import unidecode
from lxml.html.clean import clean_html
from notmuch import Database, Query
from bottle import (
    Bottle, request, response, abort, redirect, view, TEMPLATE_PATH,
    template, static_file,
)

from .mail import hierarchy, subhierarchy
from .article import reify, is_static as article_is_static

PORTAL_DIR = os.path.split(os.path.split(__file__)[0])[0]
TEMPLATE_PATH.append(os.path.join(PORTAL_DIR, 'views'))
app = Bottle()

@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@app.route('/')
@view('index')
def home():
    return {}

@app.get('/@/<querystr:path>/')
@view('thread')
def search(querystr):
    db = Database()
    query = Query(db, querystr)
    if query.count_messages() == 1:
        message = next(iter(query.search_messages()))
        title = message.get_header('subject')
        try:
            parts = [(i + 1, part.get_filename('No description')) \
                     for i, part in enumerate(message.get_message_parts())]
            body = message.get_part(1)
        except UnicodeDecodeError:
            parts = []
            body = 'There was an encoding problem with this message.'
    else:
        title = 'Results for "%s"' % querystr
        parts = []
        body = None

    return {
        'title': title,
        'parts': parts,
        'body': body,
        'threads': list(hierarchy(query)),
    }

@app.get('/@/<querystr:path>/<n:int>')
def attachment(querystr, n):
    db = Database()
    query = Query(db, querystr)
    if query.count_messages() != 1:
        redirect('/@/%s/' % querystr)
    else:
        message = next(iter(query.search_messages()))
        parts = message.get_message_parts()
        i = n - 1
        if i >= len(parts):
            redirect('/@/%s/' % querystr)
        else:
            part = parts[i]
            content_type = part.get_content_type()
            response.content_type = content_type

            fn = part.get_filename()
            if fn != None:
                response.headers['content-disposition'] = 'filename="%s";' % unidecode(fn).replace('"', '')

            payload = message.get_part(n)
            if 'html' in content_type.lower():
                return clean_html(payload)
            else:
                return payload

@app.route('/source/<filename:path>')
def source(filename):
    return static_file(filename, root = os.path.join(PORTAL_DIR, 'articles'))

ARTICLE_DIR = os.path.join(PORTAL_DIR, 'articles')
TOPDIRS = set(os.listdir(ARTICLE_DIR))

articles_cache = {}
@app.route('/!')
def article_index():
    endpoints = ('!/' + x for x in os.listdir(os.path.join(ARTICLE_DIR, '!')))
    for endpoint in endpoints:
        if endpoint not in articles_cache:
            articles_cache[endpoint] = reify(ARTICLE_DIR, endpoint)
    articles = [v for k,v in sorted(articles_cache.items()) if v != None]
    return template('exclaim-index', articles = articles)

@app.route('/<endpoint:path>')
def article(endpoint):
    if article_is_static(endpoint):
        return static_file(endpoint, root = article_dir)

    if endpoint not in articles_cache:
        articles_cache[endpoint] = reify(ARTICLE_DIR, endpoint)
    result = articles_cache[endpoint]

    if result != None:
        return template('article', result)
    else:
        return static_file(endpoint, root = article_dir)
