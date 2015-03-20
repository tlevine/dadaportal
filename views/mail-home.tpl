% rebase('base.tpl', title = "Tom's public emails")
<h1>Tom makes some emails public</h1>
<p>
  It's a lot easier for me to find things if they're on the public internet,
  and sometimes I don't even need to find things when they're there because
  other people find them for me. Also, I think that making some emails public
  will make email easier for me and reduce my need for Facebook, Twitter,
  &amp;c. I'll make it clear that I'm doing this when an email involving you
  is going to get posted here.
</p>
<p>
  It also turns out that this public email system is also a pretty convenient
  way to put any old file on the internet; just send it as an
  <a href="/!/id:20140915182359.GA28330@tlevine_vm/">attachment</a>.
</p>
<h2>Inconveniences</h2>
<p>
  Here are two things I don't like about the present library
  <a href="https://pypi.python.org/pypi/ejnug">ejnug</a>,
  which I'm calling inside the
  <a href="https://pypi.python.org/pypi/dada-portal">dada-portal</a>.
</p>
<p>
  First, although I have made some effort to hide email addresses,
  someone who knows what she is doing will still be able to find them.
  Email addresses are parts of emails, so I see this as a fundamental
  issue with email. It's perfectly fine if my email address is all over
  the internet, but other people don't share this sentiment.
</p>
<p>
  Second, if a bunch of people ran my system, we'd have a bunch of email
  websites, and it would be hard to sift through all of them. I think this
  is easier to deal with; we just need a separate thing that goes to all of
  these sites and displays all of the recent emails and perhaps figures out
  which are the most interesting. If I just expose an RSS feed of the recent
  messages, we can use ordinary RSS readers for this.
</p>
