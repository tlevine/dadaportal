import os
import logging
import enum
import json
from collections import Counter
import shutil

from . import read, render

logger = logging.getLogger(__name__)

def dadaportal():
    import horetu
    horetu.horetu({'build': build, 'index': index})

def index(src):
    tpl = render.ENV.get_template('directory.md')
    body = tpl.render(items = _index(src))
    with open(os.path.join(src, 'index.md'), 'w') as fp:
        fp.write(body)

def _index(src):
    for x in sorted(os.listdir(src)):
        y = os.path.join(src, x)
        if os.path.isdir(y):
            for srcfile, can_parse in _read(y, False):
                if can_parse and os.path.isfile(srcfile):
                    data = read.file(srcfile)
                    if 'title' in data and data.get('publish', False):
                        yield data['title'], x

def build(src, recursive:bool=False, force:bool=False):
    wd = os.path.abspath(os.path.join(__file__, '..', '..'))
    root = os.path.join(wd, 'canonical-articles')
    bang = os.path.join(root, '!') + '/'
    dest = os.path.join(wd, 'output')
    for srcfile, can_parse in _read(src, recursive):
        include_footer = srcfile.startswith(bang)
        url = os.path.relpath(srcfile, root)
        dirurl = os.path.dirname(url)

        if os.path.isdir(srcfile):
            destfile = os.path.join(dest, url, 'index.html')
            modified = None
        else:
            if can_parse:
                destfile = os.path.join(dest, dirurl, 'index.html')
            else:
                destfile = os.path.join(dest, url)
            modified = os.stat(srcfile).st_mtime

        if force or modified == None or \
            not os.path.isfile(destfile) or \
            os.stat(destfile).st_mtime < modified:

            os.makedirs(os.path.dirname(destfile), exist_ok=True)
            if can_parse:
                try:
                    if os.path.isdir(srcfile):
                        data = read.directory(srcfile)
                        slug = os.path.basename(url)
                    else:
                        data = read.file(srcfile)
                        slug = os.path.basename(dirurl)
                except Exception as e:
                    logger.traceback('Error processing %s' % fn)
                    continue
                y = render.html(data.get('title', slug),
                                data.get('description', ''),
                                data['body'], include_footer)
                with open(destfile, 'w') as fp:
                    fp.write(y)

                if include_footer:
                    y = render.slides(data.get('title', slug),
                                      data.get('description', ''),
                                      data['body'])

                slides = os.path.join(os.path.dirname(destfile), 'slides')
                os.makedirs(slides, exist_ok=True)
                with open(os.path.join(slides, 'index.html'), 'w') as fp:
                    fp.write(y)

            else:
                shutil.copy(srcfile, destfile)

def _read(x, recursive):
    if not os.path.isdir(x):
        raise TypeError('Not a directory: %s' % x)
    bn = os.path.basename(os.path.abspath(x))
    if bn == 'slides':
        raise ValueError('Directory may not be named "slides".')
    if bn.startswith('.'):
        raise StopIteration

    if recursive:
        for y in os.listdir(x):
            z = os.path.abspath(os.path.join(x, y))
            if os.path.isdir(z):
                yield from _read(z, recursive)

    n = _n_index_files(x)
    if n == 0:
        yield x, True

    if n > 1:
        logger.warn('''Multiple index files are in the directory "%s".
I am processing neither.''' % x)
    else:
        for y in os.listdir(x):
            fn = os.path.join(x, y)
            if os.path.isfile(fn):
                if read.can_read(fn):
                    yield fn, True
                else:
                    yield fn, False
    

def _n_index_files(x):
    c = Counter(fn.split('.')[0] for fn in os.listdir(x))
    return c['index']
