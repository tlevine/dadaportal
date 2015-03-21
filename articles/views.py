from django.shortcuts import render
from django.http import Http404

from .models import ArticleCache

# Create your views here.
#@app.route('/<endpoint:path>/')
def article_dynamic(request, slug):
    try:
        a = ArticleCache.objects.get(endpoint = '!/' + slug)
    except ArticleCache.DoesNotExist:
        raise Http404('No such article')
    else:
        params = a.head()
        params['body'] = a.body
        return render(request, 'article.html', params)

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
