# Documentation
Here are directions for installing (both for development and production),
for configuring external servers, and for deploying from development to
production.

## Install
Run this stuff on the server to which you are deploying (nsa).

### Install dependencies
Assuming you're on Debian,

    sudo apt-get install python3 pal notmuch python3-pip postgresql apache2 libapache2-mod-wsgi-py3
    sudo pip3 install{% for r in requirements %} {{r|safe}}{% endfor %}

### Configure the database
As the PostgreSQL user (probably "postgres"),

    createuser '{{REMOTE_USER}}'
    createdb --owner '{{REMOTE_USER}}' '{{database.NAME}}'

The database user is set to {{database.USER}}. We assume that you're using
the vanilla authentication mechanism, which is just POSIX users. Ensure that
the Apache user has access to these files, particularly if {{database.USER}}
is not the Apache user.

### Crontab
Add this crontab entry to send public emails from the email server (home)
to the production server (nsa); you must add it on *home* and *not nsa*.

    # There's a slash at the end !
    */4 * * * * rsync -avHS ~/safe/maildir/*/*/Public/*/* {{REMOTE_USER}}@{{REMOTE_SSH_HOST}}:{{REMOTE_NOTMUCH_MAILDIR}}/ && ssh www-data@nsa 'notmuch new'


### Apache
Copy this to your apache sites-enabled directory on the production computer.

    WSGIScriptAlias / {{REMOTE_BASE_DIR}}/dadaportal/wsgi.py
    WSGIPythonPath {{REMOTE_BASE_DIR}}
    WSGIDaemonProcess {{DOMAIN_NAME}} python-path={{REMOTE_BASE_DIR}}
    WSGIProcessGroup {{DOMAIN_NAME}}

    <VirtualHost {{DOMAIN_NAME}}:80>
        ServerAdmin {{EMAIL_ADDRESS}}

        <Directory {{REMOTE_BASE_DIR}}/dadaportal>
          <Files wsgi.py>
            Require all granted
          </Files>
        </Directory>

        AliasMatch ^/!/(.+/.*[^/])$ {{REMOTE_BASE_DIR}}/canonical-articles/$1

        Alias {{STATIC_URL}} {{REMOTE_STATIC_ROOT}}/
        <Directory {{REMOTE_STATIC_ROOT}}/>
            Options FollowSymLinks
            AllowOverride None
        </Directory>

        Alias /source/ {{REMOTE_BASE_DIR}}/canonical-articles/
        <Directory {{REMOTE_BASE_DIR}}/canonical-articles/>
            AllowOverride None
            Options +Indexes

            # Don't use index.html as the index page.
            DirectoryIndex
        </Directory>

        Alias /favicon.ico {{REMOTE_STATIC_ROOT}}/favicon.ico
        Alias /favicon.ico/ {{REMOTE_STATIC_ROOT}}/favicon.ico
        Alias /robots.txt {{REMOTE_STATIC_ROOT}}/robots.txt
        Alias /robots.txt/ {{REMOTE_STATIC_ROOT}}/robots.txt

        LogLevel warn
        ErrorLog ${APACHE_LOG_DIR}/dadaportal-error.log
        CustomLog ${APACHE_LOG_DIR}/dadaportal-access.log combined
    </VirtualHost>

And then reload Apache.

    sudo service apache reload

## Deploy
Run this from a computer other than the one you are deploying to.

    ./manage.py deploy

## Difficulties
Some things to consider if things are being weird.

* Check in `/etc/postgresql/9.4/main/postgresql.conf` that the typical
    port (5432) is being used.
* `ALLOWED_HOSTS` must be set appropriately.
* Turn on `DEBUG` to see what's going on.
* Run `./manage.py syncdb`.
