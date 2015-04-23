from caching import Cache

class Mail(Cache):
    message_id = m.Column(s.String, primary_key = True)
    datetime = m.Column(s.DateTime)
    thread_id = m.Column(s.String)
    filename = m.Column(s.String)
    subject = m.Column(s.String)
   #from_name = m.Column(s.String, default = '')
    from_address = m.Column(s.String, default = '')
   #recipient_names = m.Column(ARRAY(s.String, dimensions = 1), default = [])
   #recipient_addresses = m.Column(ARRAY(s.String, dimensions = 1), default = [])
    is_mailing_list = m.Column(s.Boolean)
