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

def from_html(body):
    try:
        html = lxml.html.fromstring(body)
    except lxml.etree.XMLSyntaxError:
        logger.debug('%s is not XML (It might be text.)' % path)
    else:
        data = {}
        for key, tag in [('title', 'h1'), ('description', 'p')]:
            tags = html.xpath('//' + tag)
            if len(tags) > 0:
                data[key] = tags[0].text_content()
        data['body'] = lxml.html.tostring(link_headers(link_img(html)))

    data['secret'] = head.get('secret', False)
    for key in ['redirect', 'title']:
        if key in head:
            data[key] = head[key]

    if ('title' not in data or not data['title']) and '/' not in endpoint:
        data['title'] = endpoint.replace('-', ' ')

    return data
