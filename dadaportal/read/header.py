import re
import io

from ..util import fromutf8

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

def from_html(body):
    try:
        html = fromutf8(body)
    except lxml.etree.XMLSyntaxError:
        logger.debug('%s is not XML (It might be text.)' % path)
    else:
        data = {}
        for key, tag in [('title', 'h1'), ('description', 'p')]:
            tags = html.xpath('//' + tag)
            if len(tags) > 0:
                data[key] = tags[0].text_content()
        return data
