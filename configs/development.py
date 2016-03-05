# coding: utf-8


"""Development settings."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


PASSWORD_SALT = '<Generate with `os.urandom(20)`>'

DEBUG = True

LOG_LEVEL = 'DEBUG'

SERVER_NAME = 'localhost:5000'
ELASTICSEARCH_HOST = '172.17.0.3:9200'
