cache = {}

def one_article(article_dir, endpoint):
    if endpoint not in cache:
        cache[endpoint] = reify(article_dir, endpoint)
    return cache[endpoint]

def sorted_alticles(article_dir, topdir = '!'):
    endpoints = (os.path.join(topdir, x) for x in os.listdir(os.path.join(article_dir, topdir)))
    articles_notsorted = (get_article(article_dir, endpoint) for endpoint in endpoints)
    return [v for k,v in sorted(articles_notsorted.items()) if v != None]

def all_articles(article_dir):
    for topdir in os.listdir(article_dir):
        yield from sorted_articles(os.path.join(article_dir, topdir))
