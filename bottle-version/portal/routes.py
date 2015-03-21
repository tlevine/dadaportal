import os, re

from unidecode import unidecode
from lxml.html.clean import clean_html
from bottle import (
    Bottle, request, response, abort, redirect, view, TEMPLATE_PATH,
    template, static_file,
)

from .model import Article
from .article import is_static as article_is_static

PORTAL_DIR = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
TEMPLATE_PATH.append(os.path.join(PORTAL_DIR, 'views'))
ARTICLE_DIR = os.path.join(PORTAL_DIR, 'articles')
STATIC_DIR = os.path.join(PORTAL_DIR, 'static')
ARTICLE_NOTMUCH_FROM = 'replace-this-with-a-random-thing-for-security-reasons'
app = Bottle()

#@app.hook('before_request')
#def strip_path():
#    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@app.route('/')
@view('index')
def index():
    return {}

@app.route('/@')
@app.route('/@/')
@view('mail-index')
def mail_index():
    return {}

@app.route('/source/<filename:path>/')
@app.route('/source/<filename:path>')
def source(filename):
    return static_file(filename, root = os.path.join(PORTAL_DIR, 'articles'))

# Transition to this so I can host the static files with Apache directly.
@app.route('/static/<fn:path>/')
@app.route('/static/<fn:path>')
def static(fn):
    return static_file(fn, root = STATIC_DIR)
@app.route('/img/<fn:path>/')
@app.route('/img/<fn:path>')
def static(fn):
    return static_file(fn, root = os.path.join(STATIC_DIR, 'img'))
@app.route('/css/<fn:path>/')
@app.route('/css/<fn:path>')
def static(fn):
    return static_file(fn, root = os.path.join(STATIC_DIR, 'css'))
@app.route('/js/<fn:path>/')
@app.route('/js/<fn:path>')
def static(fn):
    return static_file(fn, root = os.path.join(STATIC_DIR, 'js'))



@app.error(404)
def error404(e):
    return template('search', results = None, title = 'Page not found',
                    error404 = True)
