# This file contains local Healthchecks settings that overrides the defaults
# (/usr/lib/bundles/healthchecks/lib/python3.*/site-packages/hc/settings.py).
#
# Keep in mind that this file must be a valid Python source!
#
from hc.settings import *

import os
from urllib.parse import urlparse


# URI used to build fully qualified URLs for pings, and for use in emails and notifications.
SITE_ROOT = 'http://localhost:8000'
PING_ENDPOINT = SITE_ROOT + '/ping/'

# Name of your Healthchecks instance.
#SITE_NAME = MASTER_BADGE_LABEL = 'Mychecks'

# Domain for ping by email.
#PING_EMAIL_DOMAIN = 'localhost'

# Disable debug mode.
# Never deploy a site into production with DEBUG turned on!
DEBUG = False


#
# Database
#

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': '/var/lib/healthchecks/hc.sqlite',
#    }
#}

# Uncomment to use PostgreSQL instead of SQLite.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'healthchecks',
#         'USER': 'healthchecks',
#         'PASSWORD': 'top-secret',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'TEST': {'CHARSET': 'UTF8'}
#     }
# }


#
# Outgoing mails
#

# Email address for outgoing emails; this is where notifications will appear
# to be coming from. Make sure you set a valid domain name, otherwise the
# emails may get rejected.
#DEFAULT_FROM_EMAIL = 'healthchecks@example.org'

# The host and port of the SMTP server to use for sending email.
#EMAIL_HOST =
#EMAIL_PORT =

# Username and password to use for the SMTP server defined above.
#EMAIL_HOST_USER =
#EMAIL_HOST_PASSWORD =

# Whether to use a explicit TLS connection when talking to the SMTP server.
#EMAIL_USE_TLS = False

# Whether to use an implicit TLS connection when talking to the SMTP server.
#EMAIL_USE_SSL = False


#
# Security
#

# Hosts/domain names that are valid for this site.
# See https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    urlparse(SITE_ROOT).netloc,
    'localhost',
    '127.0.0.1',
    '[::1]',
]

# Whether registration of new accounts is currently permitted.
REGISTRATION_OPEN = False

# A secret key used for signing sessions, cookies, password reset tokens etc.
SECRET_KEY = open(os.path.join(os.path.dirname(__file__), 'secret_key')).read()

# If you're behind a proxy, use the X-Forwarded-Host header
# See https://docs.djangoproject.com/en/1.9/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if urlparse(SITE_ROOT).scheme == 'https':
    # Whether to use a secure cookie (i.e. HTTPS only) for the CSRF and session cookie.
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # And if your proxy does your SSL encoding for you, set SECURE_PROXY_SSL_HEADER
    # https://docs.djangoproject.com/en/1.9/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#
# Authentication
#

AUTHENTICATION_LDAP = False

if AUTHENTICATION_LDAP:
    import ldap
    from django_auth_ldap.config import LDAPSearch

    # The URI of the LDAP server.
    AUTH_LDAP_SERVER_URI = 'ldaps://ldap.example.org'

    # An LDAPSearch object that will locate a user in the directory.
    # The filter parameter should contain the placeholder %(user)s for the
    # username, which is an e-mail address in this case.
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        'ou=People,dc=example,dc=org',
        ldap.SCOPE_SUBTREE,
        '(mail=%(user)s)'
    )

    # A mapping from User field names to LDAP attribute names.
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    # The following should not be needed to modify.
    ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, '/etc/ssl/certs')
    AUTHENTICATION_BACKENDS += ('django_auth_ldap.backend.LDAPBackend',)


#
# Integrations
#

# Discord
#DISCORD_CLIENT_ID = None
#DISCORD_CLIENT_SECRET = None

# Slack
#SLACK_CLIENT_ID = None
#SLACK_CLIENT_SECRET = None

# Pushover
#PUSHOVER_API_TOKEN = None
#PUSHOVER_SUBSCRIPTION_URL = None
#PUSHOVER_EMERGENCY_RETRY_DELAY = 300
#PUSHOVER_EMERGENCY_EXPIRATION = 86400

# Pushbullet
#PUSHBULLET_CLIENT_ID = None
#PUSHBULLET_CLIENT_SECRET = None

# Telegram
#TELEGRAM_BOT_NAME = "ExampleBot"
#TELEGRAM_TOKEN = None

# SMS (Twilio) integration
#TWILIO_ACCOUNT = None
#TWILIO_AUTH = None
#TWILIO_FROM = None
#TWILIO_USE_WHATSAPP = False

# PagerDuty
#PD_VENDOR_KEY = None

# Trello
#TRELLO_APP_KEY = None

# Matrix
#MATRIX_HOMESERVER = None
#MATRIX_USER_ID = None
#MATRIX_ACCESS_TOKEN = None


#
# Logging
#

HC_LOG_DIR = os.getenv('HC_LOG_DIR', '/var/log/healthchecks')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file':{
            'level': 'INFO',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(HC_LOG_DIR, 'healthchecks.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}


#
# Sentry
#

SENTRY_ENABLED = os.getenv('HC_SENTRY_DSN', False)

if SENTRY_ENABLED:
    RAVEN_CONFIG = {
        # Sentry DSN (https://<key>:<secret>@host.name/<project>).
        'dsn': os.getenv('HC_SENTRY_DSN'),
    }

    # The following should not be needed to modify.
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['root']['handlers'].append('sentry')


#
# Internationalization
#

#LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'
