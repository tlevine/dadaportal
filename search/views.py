from notmuch import Database, Query

from django.conf import settings
from django.shortcuts import render

def search(request):
    if 'q' not in request.GET:
        params = {'results': None, 'title': 'Search'}
        return render(request, 'search.html', params)
    q = request.GET.get('q') # query
    p = request.GET.get('p', 1) # page

    results = []
    db = Database()
    query = Query(db, q)
    for i, m in enumerate(query.search_messages()):
        if i >= settings.MAX_SEARCH_RESULTS:
            break
        if settings.NOTMUCH_SECRET == m.get_header('from'):
            href = m.get_header('to')
        else:
            href = '/@/id:%s' % m.get_message_id()
        subject = m.get_header('subject')
        if subject.strip() == '':
            subject = settings.DEFAULT_SEARCH_RESULT_TITLE
        results.append({
            'href': href,
            'title': subject,
        })
    params = {
        'results': results,
        'q': q,
        'title': 'Results for "%s"' % q,
    }
    return render(request, 'search.html', params)
