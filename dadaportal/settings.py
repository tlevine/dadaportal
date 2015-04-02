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
from socket import gethostname
from getpass import getuser

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
if 'DATABASE_PASSWORD' in section.keys():
    PASSWORD = section['DATABASE_PASSWORD']
else:
    PASSWORD = None
for secret_name in ['NOTMUCH_SECRET', 'SECRET_KEY']:
    if secret_name not in section.keys():
        c.set(section_name, secret_name, ''.join(sample(ascii_letters + digits, 62)))
    locals()[secret_name] = c.get(section_name, secret_name)
with open(config_file, 'w') as fp:
    c.write(fp)

# This is a Unix user on nsa
REMOTE_USER = 'www-data'

# This is an SSH host, configured in .ssh/config.
REMOTE_SSH_HOST = 'nsa'

REMOTE_NOTMUCH_MAILDIR = '/var/www/maildir'

IS_PRODUCTION = getuser() == REMOTE_USER or gethostname() == REMOTE_SSH_HOST or 'USER' not in os.environ

if IS_PRODUCTION:
    DEBUG = False
    TEMPLATE_DEBUG = False

    USER = REMOTE_USER
    NOTMUCH_MAILDIR = REMOTE_NOTMUCH_MAILDIR

else:
    print('Running in development mode')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True

    if os.environ['USER'] == REMOTE_USER:
        USER = REMOTE_USER
    else:
        USER = os.environ['USER']
    NOTMUCH_MAILDIR = None

ALLOWED_HOSTS = ['127.0.0.1:*', 'localhost:*', 'thomaslevine.com:*', '.thomaslevine.com:*', 'portal.dada.pink']

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
        'HOST': 'localhost',
        'PASSWORD': PASSWORD,
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARN',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'warn.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'WARN',
            'propagate': True,
        },
    },
}


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

DO_NOT_TRACK = [
    r'^/admin',
    r'^/track',
]
