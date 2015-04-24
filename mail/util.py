import email

from unidecode import unidecode

def encode_charset(message, payload):
    for charset in filter(None, message.get_charsets()):
        try:
            encoded_payload = payload.encode(charset)
        except UnicodeEncodeError:
            pass
        else:
            encoding = charset
            break
    else:
        encoded_payload = unidecode(payload).encode('utf-8')
        encoding = 'utf-8'

    return encoding, encoded_payload

def decode_charset(message, payload):
    '''
    Decode a payload and clean the HTML if appropriate.
    '''
    if 'html' in message.get_content_type().lower():
        payload = clean_html(payload)

    for charset in filter(None, message.get_charsets()):
        try:
            decoded_payload = payload.decode(charset)
        except UnicodeEncodeError:
            pass
        else:
            break
    else:
        decoded_payload = unidecode(payload)

    return decoded_payload

def decode_header(header):
    '''
    Decode header with different encodings.
    '''
    def f(content, charset):
        if isinstance(content, str):
            return content
        elif charset == None:
            return content.decode('utf-8')
        else:
            return content.decode(charset)
    return ''.join(f(*args) for args in email.header.decode_header(header))
