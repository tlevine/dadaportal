from django.shortcuts import render

from .models import ArticleCache

# Create your views here.
#@app.route('/<endpoint:path>/')
def article_dynamic(request, endpoint):
    a = ArticleCache.objects.get(endpoint = endpoint)



    if not article_is_static(endpoint):
        result = Article.one(ARTICLE_DIR, endpoint)
        if result != None:
            return template('article', result)
    else:
        return static_file(endpoint, root = ARTICLE_DIR)
    abort(404)

#@app.route('/<endpoint:path>')
def article_static(endpoint):
    x = endpoint.lstrip('/.')
    if os.path.isfile(os.path.join(ARTICLE_DIR, x)):
        return static_file(endpoint, root = ARTICLE_DIR)
    elif os.path.isfile(os.path.join(STATIC_DIR, x)):
        # For backwards compatibility
        return static_file(endpoint, root = STATIC_DIR)
    else:
        redirect('/%s/' % endpoint)
