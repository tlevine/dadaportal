@app.route('/@')
@app.route('/@/')
@view('mail-index')
def mail_index():
    return {}

@app.error(404)
def error404(e):
    return template('search', results = None, title = 'Page not found',
                    error404 = True)
