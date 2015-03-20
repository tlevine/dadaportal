import os, re

def article_possibilities(endpoint):
    partial_directory, identifier = os.path.split(endpoint)
    directory = os.path.join(PORTAL_DIR, partial_directory)
    return [os.path.join(directory, x) for x in os.listdir(directory) \
            if _matches(identifier, x)]

def render(filename):
    extension = re.match(EXTENSION, filename).group(1)

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
