from django.shortcuts import render

def search(request):
    if 'q' not in request.params:
        params = {'results': None, title = 'Search'}
        return render(request, 'search.html', params)
    q = request.params.get('q') # query
    p = request.params.get('p', 1) # page

    start = (p - 1) * 100
    end = p * 100
    results = []
    db = Database()
    query = Query(db, q)
    for i, m in enumerate(query.search_messages()):
        if i < start:
            pass
        elif i >= end:
            break
        else:
            if ARTICLE_NOTMUCH_FROM == m.get_header('from'):
                href = m.get_header('to')
            else:
                href = '/@/id:%s' % m.get_message_id()
            subject = m.get_header('subject')
            if subject.strip() == '':
                subject = '(no subject)'
            results.append({
                'href': href,
                'title': subject,
            })
    return render(response, 'search.html', results = results, q = q,
                  title = 'Results for "%s" % q')
