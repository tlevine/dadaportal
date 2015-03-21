import os

from .article import reify

cache = {}

def one_article(article_dir, endpoint):
    if endpoint not in cache:
        cache[endpoint] = reify(article_dir, endpoint)
    return cache[endpoint]

def many_articles(article_dir, topdir = '!'):
    endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
    return (one_article(article_dir, endpoint) for endpoint in sorted(endpoints))

def all_articles(article_dir):
    for topdir in os.listdir(article_dir):
        yield from many_articles(os.path.join(article_dir, topdir))
