# coding: utf-8


"""
Default settings for seeding the config.

Each valid config entry has to be set here, so it can be accessed without
having to deal with `KeyError`s.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'configs')

# Note: changing any of these will make it impossible
#       to verify *existing* passwords.
PASSWORD_SALT = None
PASSWORD_HASH_ALGO = 'sha512'
PASSWORD_ROUNDS = 100000

DEBUG = False
TESTING = False

LOG_LEVEL = 'WARNING'

SERVER_NAME = None
ELASTICSEARCH_HOST = None
