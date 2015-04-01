from notmuch import Database, Query

from django.conf import settings
from django.shortcuts import render

def search(request):
    if 'q' not in request.GET:
        params = {'results': None, 'title': 'Search'}
        return render(request, 'search.html', params)
    q = request.GET.get('q') # query
    p = request.GET.get('p', 1) # page

    hide_emails = 'hide_emails' in request.GET
    if hide_emails:
        querystr = 'from:"%s" and %s' % (settings.NOTMUCH_SECRET, q)
    else:
        querystr = q
    db = Database(settings.NOTMUCH_MAILDIR)
    query = Query(db, querystr)

    results = []
    for i, m in enumerate(query.search_messages()):
        if i >= settings.MAX_SEARCH_RESULTS:
            break
        subject = m.get_header('subject')

        if settings.NOTMUCH_SECRET == m.get_header('from'):
            href = '/!/%s/' % m.get_header('to')
            if subject.strip() == '':
                subject = m.get_header('to')
        else:
            href = '/@/id:%s' % m.get_message_id()
            if subject.strip() == '':
                subject = settings.DEFAULT_SEARCH_RESULT_TITLE
        results.append({
            'href': href,
            'title': subject,
        })
    params = {
        'results': results,
        'hide_emails': hide_emails,
        'q': q,
        'title': 'Results for "%s"' % q,
    }
    return render(request, 'search.html', params)
