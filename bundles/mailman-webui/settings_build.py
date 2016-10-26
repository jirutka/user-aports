#-*- coding: utf-8 -*-
"""
Django settings for build (assets compilation).
"""

SECRET_KEY = 'top-secret'
STATIC_ROOT = 'static'

# django-compressor
# https://pypi.python.org/pypi/django_compressor
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sassc -t compressed {infile} {outfile}'),
    ('text/x-sass', 'sassc -t compressed {infile} {outfile}'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
