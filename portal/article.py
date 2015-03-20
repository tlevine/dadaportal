import os, re, io
import yaml, markdown, docutils.parsers

def get_possibilities(article_dir, endpoint):
    if os.path.isdir(os.path.join(article_dir, endpoint)):
        return get_possibilities(article_dir, os.path.join(endpoint, 'index'))
    partial_directory, identifier = os.path.split(endpoint)
    directory = os.path.join(article_dir, partial_directory)
    return [os.path.join(directory, x) for x in os.listdir(directory) \
            if x.startswith(identifier)]

SEPARATOR = re.compile(r'^-+$')
def parse(filename):
    formatter = FORMATS[re.match(EXTENSION, filename).group(1)]
    with open(filename) as body_fp:
        head_fp = io.StringIO()
        for line in head_fp:
            if re.match(SEPARATOR, line):
                head_fp.seek(0)
                break
            else:
                head_fp.write(line)
        data = yaml.load(head_fp)
        if not type(data) == dict:
            data = {}
        data['body'] = formatter(body_fp)
    return data

def md(fp):
    return markdown.markdown(fp.read())

FORMATS = {
    'mdwn': md,
    'md': md,
}
EXTENSION = re.compile(r'^.*\.([a-z]+)$')

def article(abort, static_file, template, article_dir, endpoint):
    m = re.match(EXTENSION, endpoint)
    if m and m.group(1) not in FORMATS:
        return static_file(endpoint, root = article_dir)

    possibilities = get_possibilities(article_dir, endpoint)
    if len(possibilities) == 1:
        return template('article', parse(possibilities[0]))
    elif len(possibilities) == 0:
        return static_file(endpoint, root = article_dir)
    elif len(possibilities) > 1:
        abort(500)
