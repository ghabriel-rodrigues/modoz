# Django settings for modoz project.

import os
PROJECT_ROOT_PATH=os.path.dirname(os.path.abspath(__file__))

DEBUG = True
myhost = os.uname()[1]

if myhost == 'ghabriel-pc':
    ONLINE = False
else:
    ONLINE = True


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

if ONLINE:

    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'devpublicon19'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'devpublicon19'             # Not used with sqlite3.
    DATABASE_PASSWORD = 'modozeromysql1'         # Not used with sqlite3.
    DATABASE_HOST = 'mysql.devpublicon.kinghost.net'             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
    SITE_ID = 2
    #URL DO REDIRECIONAMENTO DE LOGIN DA modozero
    LOGIN_REDIRECT_URL = '/modoz/'
    LOGIN_URL = '/modoz/login/'
    LOGOUT_URL = '/modoz/logout/'

else:

    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'modoz'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'             # Not used with sqlite3.
    DATABASE_PASSWORD = 'root'         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
    SITE_ID = 2
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/login/'
    LOGOUT_URL = '/logout/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'



# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media')



# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if ONLINE:
    #ADMIN_MEDIA_PREFIX = 'http://modoz.com.br/modoz/media/admin/'
    ADMIN_MEDIA_PREFIX = 'https://modozero.com.br/modoz/media/admin/'

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash if there is a path component (optional in other cases).
    # Examples: "http://media.lawrence.com", "http://example.com/media/"
    MEDIA_URL = 'https://modozero.com.br/modoz/media/'

else:
    ADMIN_MEDIA_PREFIX = 'http://127.0.0.1:8000/media/admin/'
    MEDIA_URL = '/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = '6x=l0g)pa6*l++b(%)pg(*dk=kf0dr^eb1a0zx4!64$rjapew0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",

    "contextos.utilitarios.utilidades",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'modoz.urls'

GRAPPELLI_ADMIN_TITLE = "modozero"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT_PATH,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'modoz.modulos.grappelli',
    'modoz.modulos.educacional',
    'modoz.modulos.pessoal',
    'modoz.modulos.institucional',
)
