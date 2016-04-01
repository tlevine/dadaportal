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
    horetu.horetu([build, index])

def index(src):
    for srcfile, can_parse in _read(src, False):
        if can_parse:
            data = read.file(srcfile)
            print(data)

def build(src, recursive:bool=False, force:bool=False):
    with open('.dadaportal.conf') as fp:
        conf = json.load(fp)

    for spec in conf:
        thisroot = os.path.abspath(spec['root'])
        mainroot = os.path.abspath('.')
        dest = os.path.join('.output', os.path.relpath(thisroot, '.'))
        if os.path.abspath(src).startswith(thisroot):
            _build(src, thisroot, dest, recursive,
                   render.renderers[spec['render']], force,
                   spec.get('include-footer', False))
            break
    else:
        logger.warning('No appropriate configuration was found.')

def _build(src, root, dest, recursive, renderer, force, include_footer):
    for srcfile, can_parse in _read(src, recursive):
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
                if os.path.isdir(srcfile):
                    data = read.directory(srcfile)
                    slug = os.path.basename(url)
                else:
                    data = read.file(srcfile)
                    slug = os.path.basename(dirurl)
                y = renderer(data.get('title', slug),
                             data.get('description', ''),
                             data['body'], slug, include_footer)
                with open(destfile, 'w') as fp:
                    fp.write(y)
            else:
                shutil.copy(srcfile, destfile)

def _read(x, recursive):
    if not os.path.isdir(x):
        raise TypeError('Not a directory: %s' % x)
    if os.path.basename(os.path.abspath(x)).startswith('.'):
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
