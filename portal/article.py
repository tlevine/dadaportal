import os, re, io

def possibilities(article_dir, endpoint):
    partial_directory, identifier = os.path.split(endpoint)
    directory = os.path.join(article_dir, partial_directory)
    return [os.path.join(directory, x) for x in os.listdir(directory) \
            if _matches(identifier, x)]

SEPARATOR = re.compile(r'^-+$')
def parse(filename):
    formatter = FORMATS[re.match(EXTENSION, filename).group(1)]
    with open(filename) as body_fp:
        head_fp = io.StringIO()
        for line in fp:
            if re.match(SEPARATOR, line):
                head_fp.seek(0)
                break
            else:
                head_fp.write(line)
        head = yaml.load(head_fp)
        body = formatter(body_fp)
    return {'head': head, 'body': body}

FORMATS = {
    'mdwn': markdown.markdownFromFile,
    'md': markdown.markdownFromFile,
}
EXTENSION = re.compile(r'^.*\.[a-z]+$')

def _matches(identifier, endpoint):
    if not endpoint.endswith(identifier):
        return False
    elif not re.match(EXTENSION, endpoint):
        return False
    else:
        return True
