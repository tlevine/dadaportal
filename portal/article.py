import os, functools, re

def article(endpoint):
    partial_directory, identifier = os.path.split(endpoint)
    directory = os.path.join(PORTAL_DIR, partial_directory)
    possibilities = [os.path.join(directory, x) for x in os.listdir(directory) \
                     if _matches(identifier, x)]
    if len(possibilities) == 1:
        return _render(possibilities[0])
    elif len(possibilities) > 1:
        abort(500)
    else:
        abort(404)

FORMATS = {
    'mdwn': markdown.markdown,
    'md': markdown.markdown,
}
EXTENSION = re.compile(r'^.*\.[a-z]+$')

def _matches(identifier, endpoint):
    if not endpoint.endswith(identifier):
        return False
    elif not re.match(EXTENSION, endpoint):
        return False
    else:
        return True
