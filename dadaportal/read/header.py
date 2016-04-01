import re
import io

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
    return head_fp, io.StringIO(body_fp.read())

def from_html(html):
    data = {}
    for key, tag in [('title', 'h1'), ('description', 'p')]:
        tags = html.xpath('//' + tag)
        if len(tags) > 0:
            data[key] = tags[0].xpath('string()')
    return data
