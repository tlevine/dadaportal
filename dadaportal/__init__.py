import os
import logging
import enum
import json
from collections import Counter
import shelve

from . import read, render

logger = logging.getLogger(__name__)

def dadaportal():
    import horetu
    horetu.horetu(build)

def build(src, recursive:bool=False):
    with open('.dadaportal.conf') as fp:
        conf = json.load(fp)

    for spec in conf:
        if os.path.abspath(src).startswith(os.path.abspath(spec['root'])):
            _build(src, spec['root'], spec['destination'], recursive)
            break
    else:
        logger.warning('No appropriate configuration was found.')

def _build(src, root, dest, recursive):
    index = shelve.open(os.path.join(root, '.index'))
    for srcfile, can_parse in _read(src, recursive):
        url = os.path.relpath(srcfile, root)
        destfile = os.path.join(dest, url)
        if not os.path.isfile(destfile) or \
            os.stat(destfile).st_mtime < os.stat(srcfile).st_mtime:
            if can_parse:
                data = read.file(srcfile)
                y = f(data['title'], data['description'], data['body'])
                with open(destfile, 'w') as fp:
                    fp.write(y)
                if not data['secret']:
                    index[url] = data['title']
            else:
                shutil.copy(srcfile, destfile)
    index.close()

def _read(x, recursive):
    if not os.path.isdir(x):
        raise TypeError('Not a directory: %s' % x)
    if x.startswith('.'):
        raise StopIteration

    if recursive:
        for y in os.listdir(x):
            if os.path.isdir(y):
                yield from _read(os.path.abspath(os.path.join(x, y)),
                                 recursive)

    if _multiple_index_files(x):
        logger.warn('''Multiple index files are in the directory "%s".
I am processing neither.''' % x)
    else:
        for y in os.listdir(x):
            fn = os.path.join(x, y)
            if os.path.isfile(fn):
                if read.can_read(fn):
                    yield fn, True
                    break
                else:
                    yield fn, False
        else:
            tpl = 'No valid index files found the directory "%s".'
            logger.warn(tpl % x)
    

def _multiple_index_files(x):
    c = Counter(fn.split('.')[0] for fn in os.listdir(x))
    return c['index'] > 1
