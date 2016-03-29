import logging
from collections import Counter

from . import read, render

logger = logging.getLogger(__name__)

def build(src, dest, recursive:bool=False):
    for srcfile, data in _read(src, recursive):
        destfile = os.path.join(dest, os.path.relpath(srcfile, src))
        if data:
            raise NotImplementedError('Render to %s' % destfile)
        else:
            shutil.copy(srcfile, destfile)

def _read(x, recursive):
    if not os.path.isdir(x):
        raise TypeError('Not a directory: %s' % x)

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
            if os.path.isfile(y):
                fn = os.path.join(x, y)
                z = read.file(fn)
                if z:
                    yield fn, z
                    break
                else:
                    yield fn, None
        else:
            tpl = 'No valid index files found the directory "%s".'
            logger.warn(tpl % x)
    

def _multiple_index_files(x):
    c = Counter(fn.split('.')[0] for fn in os.listdir(x))
    return c['index'] > 1
