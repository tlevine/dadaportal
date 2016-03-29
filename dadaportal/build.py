def directory(x):
    if not os.path.isdir(x):
        raise TypeError('Not a directory: %s' % x)
    for fn in os.listdir(x):
        if os.path.isdir(x):

