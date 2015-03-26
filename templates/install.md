# Documentation
Here are directions for installing (both for development and production),
for configuring external servers, and for deploying from development to
production.

## Install dependencies
Assuming you're on Debian,

    sudo apt-get install python3 pal notmuch python3-pip postgresql
    sudo pip3 install{% for r in requirements %} {{r}}{% endfor %}

## Configure the database
As the PostgreSQL user (probably "postgres"),

    createuser '{{database.USER}}'
    createdb --owner '{{web_user}}'  '{{database.NAME}}'

The database user is set to {{database.USER}}. We assume that you're using
the vanilla authentication mechanism, which is just POSIX users. Ensure that
the Apache user has access to these files, particularly if {{database.USER}}
is not the Apache user.

## Crontab
Add this crontab entry to send public emails from the email server (home)
to the production server (nsa); you must add it on *home* and *not nsa*.

    */4 * * * * rsync -avHS ~/safe/maildir/*/*/Public/*/* nsa:{{notmuch_dir}}/

'

## Apache
Copy this to your apache sites-enabled directory on the production computer.

    <VirtualHost {{DOMAIN_NAME}}:80>
        ServerAdmin _@thomaslevine.com

        DocumentRoot {{STATIC_ROOT}}
        <Directory {{STATIC_URL}}>
            Options FollowSymLinks
            AllowOverride None
        </Directory>

        LogLevel warn
        ErrorLog ${APACHE_LOG_DIR}/dadaportal-error.log
        CustomLog ${APACHE_LOG_DIR}/dadaportal-access.log combined
    </VirtualHost>

And then reload Apache.

    sudo service apache reload
