def split(body_fp):
    head_fp = io.StringIO()
    for line in body_fp:
        if re.match(r'^-+\s+$', line):
            # Dashed line
            head_fp.seek(0)
            break
        elif re.match(r'^\s*$', line):
            # Empty line before a dashed line
            head_fp.truncate(0)
            body_fp.seek(0)
            break
        else:
            head_fp.write(line)
    else:
        # If there was no dashed line,
        head_fp.truncate(0)
        body_fp.seek(0)
    return head_fp, body_fp





    title = models.TextField(null = True)
    description = models.TextField(null = True)
    body = models.TextField(null = False)

    redirect = models.TextField(null = True)
    tagsjson = models.TextField(null = False) # JSON
    secret = models.BooleanField(null = False, default = False)
    tags
