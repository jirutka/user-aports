#-*- coding: utf-8 -*-
"""
Django settings for HyperKitty + Postorius

Pay attention to settings ALLOWED_HOSTS and DATABASES!
"""
from os.path import abspath, dirname, join as joinpath
from ConfigParser import SafeConfigParser


def read_cfg(path, section=None, option=None):
    config = SafeConfigParser()
    config.read(path)
    def get(section, option):
        return config.get(section, option) if config.has_option(section, option) else None
    return get(section, option) if section else get

mailman_cfg = read_cfg('/etc/mailman.cfg')


BASE_DIR = '/usr/lib/bundles/mailman-webui'
CONF_DIR = '/etc/mailman-webui'
DATA_DIR = '/var/lib/mailman-webui'
LOG_DIR = '/var/log/mailman-webui'

# Hosts/domain names that are valid for this site.
# NOTE: You MUST add domain name of your instance of this application here!
# See https://docs.djangoproject.com/en/1.9/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost']

# Mailman API credentials
# NOTE: Replace with hard-coded values if Mailman is running on a different host.
MAILMAN_REST_API_URL = 'http://localhost:%s' % (mailman_cfg('webservice', 'port') or 8001)
MAILMAN_REST_API_USER = mailman_cfg('webservice', 'admin_user') or 'restadmin'
MAILMAN_REST_API_PASS = mailman_cfg('webservice', 'admin_pass')
MAILMAN_ARCHIVER_KEY = read_cfg('/etc/mailman.d/hyperkitty.cfg', 'general', 'api_key')
MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1', '::ffff:127.0.0.1')

# Only display mailing-lists in HyperKitty from the same virtual host
# as the webserver.
FILTER_VHOST = False


#
# Application definition
#

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'hyperkitty',
    'rest_framework',
    'django_gravatar',
    'paintstore',
    'compressor',
    'haystack',
    'django_extensions',
    'postorius',
    'django_mailman3',

    # Uncomment the next line to enable integration with Sentry
    # and set DSN in RAVEN_CONFIG.
    #'raven.contrib.django.raven_compat',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Uncomment providers that you want to use, if any.
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.gitlab',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.stackexchange',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'hyperkitty.middleware.SSLRedirect',
    'django_mailman3.middleware.TimezoneMiddleware',
    'postorius.middleware.PostoriusMiddleware',
)

# A string representing the full Python import path to your root URLconf.
ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Directory for templates override.
            joinpath(DATA_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mailman3.context_processors.common',
                'hyperkitty.context_processors.common',
                'postorius.context_processors.postorius',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Using the cache infrastructure can significantly improve performance on a
# production setup. This is an example with a local Memcached server.
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}


#
# Databases
# See https://docs.djangoproject.com/en/1.9/ref/settings/#databases
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': joinpath(DATA_DIR, 'db.sqlite3'),
    }
# Remove the above lines and uncomment the below to use PostgreSQL.
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'mailman_webui',
#        'USER': 'mailman_webui',
#        'PASSWORD': 'change-me',
#        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#        'HOST': '127.0.0.1',
#        'PORT': '',
#    }
}

# Full-text search engine
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': joinpath(DATA_DIR, 'fulltext_index'),
    },
}


#
# Outgoing mails
#

# NOTE: Replace with hard-coded values if Mailman is running on a different host.

# The host and port of the SMTP server to use for sending email.
EMAIL_HOST = mailman_cfg('mta', 'smtp_host') or 'localhost'
EMAIL_PORT = int(mailman_cfg('mta', 'smtp_port') or 25)

# Username and password to use for the SMTP server defined above.
EMAIL_HOST_USER = mailman_cfg('mta', 'smtp_user') or ''
EMAIL_HOST_PASSWORD = mailman_cfg('mta', 'smtp_pass') or ''

# Whether to use a explicit TLS connection when talking to the SMTP server.
EMAIL_USE_TLS = False

# Whether to use an implicit TLS connection when talking to the SMTP server.
EMAIL_USE_SSL = False

# A tuple that lists people who get code error notifications. When DEBUG=False
# and a view raises an exception, Django will email these people with the full
# exception information. Each member of the tuple should be a tuple of (Full
# name, email address).
ADMINS = (
     ('Mailman Admin', 'root@localhost'),
)

# If you enable email reporting for error messages, this is where those emails
# will appear to be coming from. Make sure you set a valid domain name,
# otherwise the emails may get rejected.
# https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-SERVER_EMAIL
#SERVER_EMAIL = 'root@your-domain.org'

# If you enable internal authentication, this is the address that the emails
# will appear to be coming from. Make sure you set a valid domain name,
# otherwise the emails may get rejected.
# https://docs.djangoproject.com/en/1.9/ref/settings/#default-from-email
#DEFAULT_FROM_EMAIL = 'mailing-lists@you-domain.org'


#
# Security settings
#

# A secret key used for signing sessions, cookies, password reset tokens etc.
SECRET_KEY = open(joinpath(CONF_DIR, 'secret_key')).read()

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# If you're behind a proxy, use the X-Forwarded-Host header
# See https://docs.djangoproject.com/en/1.9/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = True

# And if your proxy does your SSL encoding for you, set SECURE_PROXY_SSL_HEADER
# https://docs.djangoproject.com/en/1.9/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#SECURE_SSL_REDIRECT = True

# If you set SECURE_SSL_REDIRECT to True, make sure the SECURE_REDIRECT_EXEMPT
# contains at least this line:
#SECURE_REDIRECT_EXEMPT = [
#    'archives/api/mailman/.*',  # Request from Mailman.
#]


#
# Authentication
#

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # Uncomment to next line to enable LDAP authentication.
    #'django_auth_ldap.backend.LDAPBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'hk_root'
LOGOUT_URL = 'account_logout'

# Whether registration of new accounts is currently permitted.
REGISTRATION_OPEN = True

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

## Django Allauth

# Custom AccountAdapter for allauth that respects REGISTRATION_OPEN variable.
ACCOUNT_ADAPTER = 'custom.CloseableRegistrationAccountAdapter'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_UNIQUE_EMAIL  = True

SOCIALACCOUNT_PROVIDERS = {}
#SOCIALACCOUNT_PROVIDERS = {
#    'openid': {
#        'SERVERS': [
#            {
#                'id': 'yahoo',
#                'name': 'Yahoo',
#                'openid_url': 'http://me.yahoo.com'
#            }
#        ],
#    },
#    'google': {
#        'SCOPE': ['profile', 'email'],
#        'AUTH_PARAMS': {'access_type': 'online'},
#    },
#    'facebook': {
#       'METHOD': 'oauth2',
#       'SCOPE': ['email'],
#       'FIELDS': [
#           'email',
#           'name',
#           'first_name',
#           'last_name',
#           'locale',
#           'timezone',
#       ],
#       'VERSION': 'v2.4',
#    },
#}

## Django LDAP
if 'allauth.account.auth_backends.AuthenticationBackend' in AUTHENTICATION_BACKENDS:
    import ldap
    from django_auth_ldap.config import LDAPSearch

    ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, '/etc/ssl/certs')

    AUTH_LDAP_SERVER_URI = 'ldaps://ldap.example.org'

    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        'ou=People,dc=example,dc=org',
        ldap.SCOPE_SUBTREE,
        '(&(mail=*)(uid=%(user)s))'
    )

    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }


#
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
#

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


#
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
#

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = joinpath(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static".
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# django-compressor
COMPRESS_OFFLINE = True

# Compatibility with Bootstrap 3
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


#
# Gravatar
# https://github.com/twaddington/django-gravatar
#

# Gravatar base url.
GRAVATAR_URL = 'http://cdn.libravatar.org/'
# Gravatar base secure https url.
GRAVATAR_SECURE_URL = 'https://seccdn.libravatar.org/'
# Gravatar size in pixels.
#GRAVATAR_DEFAULT_SIZE = '80'
# An image url or one of the following: 'mm', 'identicon', 'monsterid', 'wavatar', 'retro'.
GRAVATAR_DEFAULT_IMAGE = 'retro'
# One of the following: 'g', 'pg', 'r', 'x'.
#GRAVATAR_DEFAULT_RATING = 'g'
# True to use https by default, False for plain http.
GRAVATAR_DEFAULT_SECURE = True


#
# Logging
#

# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500 error
# when DEBUG=False. See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file':{
            'level': 'INFO',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': joinpath(LOG_DIR, 'mailman-webui.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        #'django.request': {
        #    'handlers': ['mail_admins'],
        #    'level': 'ERROR',
        #    'propagate': True,
        #},
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'postorius': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'hyperkitty': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

if 'raven.contrib.django.raven_compat' in INSTALLED_APPS:
    RAVEN_CONFIG = {
        'dsn': 'https://<key>:<secret>@sentry.io/<project>',
    }
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['root']['handlers'].append('sentry')


try:
    from settings_local import *
except ImportError:
    pass
