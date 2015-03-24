Install dependencies

    sudo apt-get install python3 pal notmuch python3-pip postgresql
    sudo pip3 install{% for r in requirements %} {{r}}{% endfor %}

# Configure the database
As the PostgreSQL user (probably "postgres"),

    createuser '{{database.USER}}'
    createdb --owner '{{web_user}}'  '{{database.NAME}}'


The database user is set to {{database.USER}}. We assume that you're using
the. Ensure that the Apache user has access
to these files, particularly if WEB_USER is not the Apache user.

Add this crontab entry to send public emails from the email server (home)
to nsa; you must copy it to the computer that contains your emails.

    */4 * * * * rsync -avHS ~/safe/maildir/*/*/Public/*/* nsa:{{notmuch_dir}}/

'
