#!/usr/bin/env python3
#
# Convert articles into email format for indexing by notmuch.
#
import sys, os
sys.path.insert(0, '.')

from portal.model import many_articles
from portal.routes import ARTICLE_DIR, template

NOTMUCH_DIR = '/tmp/articles'
for article in many_articles(ARTICLE_DIR):
    fn = os.path.join(NOTMUCH_DIR, article['endpoint'])
    dn = os.path.split(fn)[0]
    if not os.path.isdir(dn):
        os.makedirs(dn)
    with open(fn, 'w') as fp:
        fp.write(template('article-notmuch', article))

@app.route('/@')
@app.route('/@/')
@view('mail-index')
def mail_index():
    return {}

