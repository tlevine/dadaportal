"""
Django settings for dadaportal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from random import sample
from string import ascii_letters, digits
from configparser import ConfigParser, NoOptionError
import subprocess
import datetime
import os

# Dada portal repository directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Store secrets elsewhere in ~/.dadaportal configuration file.
config_file = os.path.join(BASE_DIR, '.secrets')
section_name = 'secrets'
c = ConfigParser()
c.read(config_file)
if section_name not in c.sections():
    c.add_section(section_name)
section = c[section_name]
for secret_name in ['NOTMUCH_SECRET', 'SECRET_KEY']:
    if secret_name not in section.keys():
        c.set(section_name, secret_name, ''.join(sample(ascii_letters + digits, 62)))
    locals()[secret_name] = c.get(section_name, secret_name)
with open(config_file, 'w') as fp:
    c.write(fp)

# This is a hostname.
p = subprocess.Popen(['hostname'], stdout = subprocess.PIPE)
p.wait()
LOCAL_HOST = p.stdout.read().strip()

# This is a Unix user on nsa
REMOTE_USER = 'www-data'

# This is a hostname.
REMOTE_HOST = 'nsa'

# This is an SSH host, configured in .ssh/config.
REMOTE_SSH_HOST = 'nsa'

IS_PRODUCTION = LOCAL_HOST == REMOTE_HOST and 'USER' not in os.environ

if IS_PRODUCTION:
    print('Running in production mode')
    DEBUG = False
    TEMPLATE_DEBUG = False

    USER = REMOTE_USER

else:
    print('Running in development mode')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True

    USER = os.environ['USER']

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   #'django.contrib.markup',
    'articles',
    'search',
    'mail',
    'tracking',
    'dadaportal',
)

MIDDLEWARE_CLASSES = (
    'tracking.middleware.TrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dadaportal.urls'

WSGI_APPLICATION = 'dadaportal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dadaportal',
        'USER': USER,
        'HOST': 'localhost'
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = False
TIME_ZONE = 'UTC' # That's how Tom rolls.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-compiled')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
ARTICLES_DIR = os.path.join(BASE_DIR, 'canonical-articles')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'tracking.context_processors.tracking',
)

# For tracking
HIT_ID_SIZE = 62

# For mail and searching
DEFAULT_SEARCH_RESULT_TITLE = '(no subject)'
MAX_SEARCH_RESULTS = 100
BEGINNING_OF_TIME = datetime.datetime(1990, 3, 30)
DOMAIN_NAME = 'thomaslevine.com'
NAME = 'Thomas Levine'
EMAIL_ADDRESS = '_@thomaslevine.com'
NOTMUCH_OTHER_EMAIL = 'underscore@thomaslevine.com;occurrence@thomaslevine.com;perluette@thomaslevine.com;tkl22@cornell.edu;'

# For copying files during deployment
LOCAL_PAL_DIR = os.path.expanduser('~/git/schedule')
REMOTE_PAL_DIR = '.pal'
REMOTE_BASE_DIR = '/srv/dadaportal'

REMOTE_STATIC_ROOT = os.path.join(REMOTE_BASE_DIR, 'static-compiled')

NOTMUCH_MAILDIR = os.path.join(BASE_DIR, 'maildir')
REMOTE_NOTMUCH_MAILDIR = os.path.join(REMOTE_BASE_DIR, 'maildir')
