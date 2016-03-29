# Documentation
Here are directions for downloading the Dada Portal software,
for installing (both for development and production),
for configuring external servers, and for deploying from development to
production.

## Download
If you're Tom, you can do this.

    git clone nsa:dada.pink/dadaportal

If you're someone else, you have to do this.

    git clone git@github.com:tlevine/dada-portal

## Install for development
This first section is all you need for installing the system for development
purposes.

### Install dependencies
Assuming you're on Debian,

    sudo apt-get install python3 python3-pip postgresql
    sudo pip3 install{% for r in requirements %} {{r|safe}}{% endfor %}

You can install the following by pip or by apt-get; they might take a while to build
if you use pip.

    sudo apt-get install python3-lxml python3-psycopg2
    # or
    sudo pip3 install lxml psycopg2

### Configure the database
As the PostgreSQL user (probably &ldquo;postgres&rdquo;),

    createuser '{{REMOTE_USER}}'
    createdb --owner '{{REMOTE_USER}}' '{{database.NAME}}'

The database user is set to {{database.USER}}. We assume that you're using
the vanilla authentication mechanism, which is just POSIX users.

## Install for production
To install for production, do everything in the "Install for development"
section and then do everything in the present section.

### Crontab
Add this crontab entry to send public emails from the email server (home)
to the production server (nsa); you must add it on *home* and *not nsa*.

    # There's a slash at the end!
    */4 * * * * rsync -avHS ~/safe/maildir/*/*/Public/cur/* {{REMOTE_USER}}@{{REMOTE_SSH_HOST}}:{{REMOTE_MAIL_DIR}}/ && ssh www-data@nsa 'cd {{REMOTE_BASE_DIR}} && ./manage.py update_cache && ./manage.py update_index'

### Apache
Install Apache.

    apache2 libapache2-mod-wsgi-py3

Then copy this to the apache `sites-enabled` directory on the production computer.

    WSGIScriptAlias / {{REMOTE_BASE_DIR}}/dadaportal/wsgi.py
    WSGIPythonPath {{REMOTE_BASE_DIR}}
    WSGIDaemonProcess {{DOMAIN_NAME}} python-path={{REMOTE_BASE_DIR}}
    WSGIProcessGroup {{DOMAIN_NAME}}

    <VirtualHost *:80>
        ServerName {{DOMAIN_NAME}}
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

And then reload Apache on that computer.

    sudo service apache reload

## Deploy
You should install the development version on the computer on which you
will edit the site and the production version on the computer from which
you will serve the site.

After you edit the site on the development installation, you might want
to send your edits to the production installation. To do that, run the
following command on the development computer, from the root directory
of the Dada Portal repository.

    ./manage.py deploy

## Writing emails
Add the linked [vim macro](dadamail.vim) to your `.vimrc` to sign a
message with its future address on the web. Once you have loaded the
macro, press "E" on the email draft screen in mutt to open the full
view of the email, with headers, then press "m" in normal mode in vim.

## Difficulties
Some things to consider if things are being weird.

* Check in `/etc/postgresql/9.4/main/postgresql.conf` that the typical
    port (5432) is being used.
* `ALLOWED_HOSTS` must be set appropriately.
* Turn on `DEBUG` to see what's going on.
* Run `./manage.py syncdb`.
* Ensure that the Apache user has access to the various file data sources,
    particularly if {{database.USER}} is not the Apache user.
