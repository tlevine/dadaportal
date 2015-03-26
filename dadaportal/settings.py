"""
Django settings for dadaportal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import subprocess
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

p = subprocess.Popen(['hostname'], stdout = subprocess.PIPE)
p.wait()
is_production = p.stdout.read().strip() == 'nsa'

if is_production:
    NOTMUCH_SECRET = 'maorh023h.ucrhu02hrs' # For separating emails from other
    SECRET_KEY = 'g-$dx5y31pxfu8bgr%llpnt^4&j*m%#z5eijd7&^-h#rk(xqa('

    DEBUG = False
    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = ['localhost']
    NOTMUCH_MAILDIR = os.path.join(BASE_DIR, 'maildir')

else:
    # Keep this secret on production
    NOTMUCH_SECRET = 'maorh023h.ucrhu02hrs' # For separating emails from other

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'g-$dx5y31pxfu8bgr%llpnt^4&j*m%#z5eijd7&^-h#rk(xqa('

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []
    NOTMUCH_MAILDIR = '/tmp/dadaportal-notmuch'

# Application definition

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
        'USER': os.environ['USER'],
        'HOST': 'localhost'
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

HIT_ID_SIZE = 62

DEFAULT_SEARCH_RESULT_TITLE = '(no subject)'
MAX_SEARCH_RESULTS = 100

BEGINNING_OF_TIME = datetime.datetime(1990, 3, 30)
DOMAIN_NAME = 'http://thomaslevine.com/'
NAME = 'Thomas Levine'
EMAIL_ADDRESS = '_@thomaslevine.com'
NOTMUCH_OTHER_EMAIL = 'underscore@thomaslevine.com;occurrence@thomaslevine.com;perluette@thomaslevine.com;tkl22@cornell.edu;'

REMOTE_HOST = 'nsa' # This is an SSH host, configured in .ssh/config

LOCAL_PAL_DIR = '~/.pal/p'
REMOTE_PAL_DIR = '~/.pal'

REMOTE_BASE_DIR = '/var/www/dada-portal'
CONFIGURATION_FILES_DIR = os.path.join(BASE_DIR, 'config')
