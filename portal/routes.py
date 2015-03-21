import os, re

from unidecode import unidecode
from lxml.html.clean import clean_html
from notmuch import Database, Query
from bottle import (
    Bottle, request, response, abort, redirect, view, TEMPLATE_PATH,
    template, static_file,
)

from .mail import hierarchy, subhierarchy
from .model import sorted_articles
from .article import is_static as article_is_static

PORTAL_DIR = os.path.split(os.path.split(__file__)[0])[0]
TEMPLATE_PATH.append(os.path.join(PORTAL_DIR, 'views'))
ARTICLE_DIR = os.path.join(PORTAL_DIR, 'articles')
app = Bottle()

@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@app.route('/')
@view('index')
def home():
    return {}

RECENT = '/@/date:2D..'
EMPTY_QUERY = re.compile(r'^\s*$')
@app.get('/@/<querystr:path>')
@view('thread')
def search(querystr):
    if re.match(EMPTY_QUERY, querystr):
        redirect(RECENT)
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
    if re.match(EMPTY_QUERY, querystr):
        redirect(RECENT)
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

@app.route('/!')
def article_index():
    return template('exclaim-index', articles = sorted_articles(ARTICLE_DIR, '!'))

@app.route('/<endpoint:path>')
def article(endpoint):
    if article_is_static(endpoint):
        return static_file(endpoint, root = article_dir)

    result = one_article(endpoint)

    if result != None:
        return template('article', result)
    else:
        return static_file(endpoint, root = article_dir)

@app.route('/+')
def search():
    if 'q' not in request.params:
        redirect('/+')
    q = request.params.get('q') # query
    p = request.params.get('p', 1) # page
