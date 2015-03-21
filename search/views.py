from django.shortcuts import render

# Create your views here.

@app.route('/+/')
@app.route('/+')
def search():
    if 'q' not in request.params:
        return template('search', results = None, title = 'Search',
                        error404 = response.status == 404)
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
    return template('search', results = results, q = q,
                    title = 'Results for "%s" % q')
