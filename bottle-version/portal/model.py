import os

from sqlalchemy.ext.declarative import declarative_base, declared_attr
Base = declarative_base()
import sqlalchemy as s

from .article import reify

cache = {}

class Article:
    @staticmethod
    def one(article_dir, endpoint):
        if endpoint not in cache:
            cache[endpoint] = reify(article_dir, endpoint)
        return cache[endpoint]

    @staticmethod
    def many(article_dir, topdir = '!'):
        endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
        return (Article.one(article_dir, endpoint) for endpoint in sorted(endpoints))

    @staticmethod
    def all(article_dir):
        for topdir in os.listdir(article_dir):
            yield from Article.many(os.path.join(article_dir, topdir))

# SQL Alchemy?
class Hit(Base):
    'Hit on a webpage, combining information from the HTML (or other) page and the XHR'
    __tablename__ = 'hit'

    # Populated on the first request
    id = s.Column(s.BigInteger, primary_key = True)
    session = s.Column(nullable = False)
    datetime = s.Column(s.DateTime, nullable = False)
    ip_address = s.Column(nullable = False)
    user_agent = s.Column(s.String, nullable = False)
    referrer = s.Column(s.String, nullable = False) # blank if none

    # Populated on the subsequent XHR, updated every few seconds
    screen_width = s.Column(s.Integer, nullable = True)
    screen_height = s.Column(s.Integer, nullable = True)
    seconds_on_page = s.Column(s.Integer, nullable = True)

    def insert_primary():
        pass

    def insert_js():
        pass

class ArticleHitCounts(Base):
    '''
    This table has a row for each article and hour, and a column for hit
    counts for the past few days. It can be generated fully the contents
    of the "hit" table.
    '''
    __tablename__ = 'article_statistics'

    # With the trailing slash
    endpoint = s.Column(s.String, primary_key = True)

    day_0 = s.Column(s.Integer, nullable = False) # today
    day_1 = s.Column(s.Integer, nullable = False) # yesterday
    day_2 = s.Column(s.Integer, nullable = False)
    day_3 = s.Column(s.Integer, nullable = False)
    day_4 = s.Column(s.Integer, nullable = False)
    day_5 = s.Column(s.Integer, nullable = False)
    day_6 = s.Column(s.Integer, nullable = False) # a week ago, rounded down
    day_7 = s.Column(s.Integer, nullable = False) # a week ago, rounded up

    @classmethod
    def shift(Klass):
        'Klass.day_7 is set to Klass.day_6, and so on.'
        pass


class Search(Base):
    '''
    This table has a row for each article and a column for each of several
    statistics. It can be generated fully from the contents of the "hit" table.
    '''
    __tablename__ = 'search'
    hit = s.Column(s.BigInteger, s.ForeignKey(Hit.id), primary_key = True)
    terms = s.Column(s.String, nullable = False)
    email_only = s.Column(s.Boolean, nullable = False)
    n_results = s.Column(s.Integer, nullable = False)
