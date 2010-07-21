# Django settings for hiredly project.
# 20091119 - Modified from http://code.djangoproject.com/attachment/ticket/2131/httpresponsesendfile-no-default-content_bypass-middleware_with-header_with-docs-and-tests.diff

import os
import socket
from decimal import *
import sys
import private_settings as ps

deployment_dir  = os.path.realpath(os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))))
deployment_time = deployment_dir.split("/")[-1]

sys.path.insert(0,  os.path.realpath(os.path.join(os.path.dirname(__file__), 'dependencies')))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'core', 'lib', 'python')))

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

def rel(*x):
    """Returns the current filepath with the given filename appended"""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

APPNAME = 'goswarm.net'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Bartosz', 'toszter@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''          # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/')
MEDIA_URL = '/static/'
if deployment_time.endswith("Z"):
    MEDIA_URL = "http://cdn.ytdupdate.com.s3.amazonaws.com/%s/static/" % deployment_time
ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/')
ADMIN_MEDIA_PREFIX = '/admin_media/'
if deployment_time.endswith("Z"):
   ADMIN_MEDIA_PREFIX = "http://cdn.ytdupdate.com.s3.amazonaws.com/%s/static/admin/" % deployment_time

# Make this unique, and don't share it with anybody.
SECRET_KEY = ps.SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows
    # Don't forget to use absolute paths, not relative paths.
    rel('templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'swarm.apps.base',
    'swarm.apps.compress',
    'swarm.apps.profiles',
    'swarm.apps.registration',
)

ROOT_URLCONF = 'swarm.urls'

# registration app
ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_USE_TLS = True
EMAIL_HOST = ps.EMAIL_HOST
EMAIL_HOST_USER = ps.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ps.EMAIL_HOST_PASSWORD
EMAIL_PORT = ps.EMAIL_PORT
DEFAULT_FROM_EMAIL = ps.DEFAULT_FROM_EMAIL

# profiles
AUTH_PROFILE_MODULE = "profiles.UserProfile"

# logging
INTERNAL_IPS = ('127.0.0.1',)

# media compression
COMPRESS_AUTO = True
COMPRESS_VERSION = True
COMPRESS_JS_FILTERS = []
COMPRESS_CSS_FILTERS = []

# default login, but editable
LOGIN_REDIRECT_URL = "/"

# recaptcha pub and priv keys
RECAPTCHA_PUB_KEY = ps.RECAPTCHA_PUB_KEY
RECAPTCHA_PRIV_KEY = ps.RECAPTCHA_PRIV_KEY

DEFAULT_FILE_STORAGE = ps.DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY = ps.AWS_ACCESS_KEY
AWS_SECRET_KEY = ps.AWS_SECRET_KEY
AWS_BUCKET = ps.AWS_BUCKET
AWS_PREFIX = ps.AWS_PREFIX