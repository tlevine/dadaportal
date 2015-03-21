import os

from .article import reify

cache = {}

class Article:
    @classmethod
    def one(article_dir, endpoint):
        if endpoint not in cache:
            cache[endpoint] = reify(article_dir, endpoint)
        return cache[endpoint]

    @classmethod
    def many(article_dir, topdir = '!'):
        endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
        return (Article.one(article_dir, endpoint) for endpoint in sorted(endpoints))

    @classmethod
    def all(article_dir):
        for topdir in os.listdir(article_dir):
            yield from Article.many(os.path.join(article_dir, topdir))
