def link_img(html):
    for img in html.xpath('//img[not(../self::a)]'):
        a = lxml.html.Element('a', href = img.xpath('@src')[0])
        parent = img.getparent()
        parent.replace(img, a)
        a.append(img)
    return html

def link_headers(html):
    x = '//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]'
    for h in html.xpath(x):
        if not h.text:
            continue
        if 'id' not in h.attrib:
            h.attrib['id'] = h.text.lower().replace(' ', '-')
        a = lxml.html.Element('a', href = '#' + h.attrib['id'])
        parent = h.getparent()
        parent.replace(h, a)
        a.append(h)
    return html
