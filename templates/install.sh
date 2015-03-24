#!/bin/sh
set -e

# Install dependencies
sudo apt-get install python3 pal notmuch python3-pip
sudo pip3 install{% for r in requirements %} {{r}}{% endfor %}

# Further directions
echo 'Ensure that the Apache user has access to these files
(in case WEB_USER is a different user from the Apache user.

Add this crontab entry to send public emails from the email server (home)
to nsa; you must copy it to the computer that contains your emails.

    */4 * * * * rsync -avHS ~/safe/maildir/*/*/Public/*/* nsa:{{notmuch_dir}}/

'
