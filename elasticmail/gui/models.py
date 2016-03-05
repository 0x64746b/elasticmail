# coding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from binascii import hexlify
from hashlib import pbkdf2_hmac

import elasticsearch_dsl as dsl
from flask import current_app as app


class User(dsl.DocType):

    user_name = dsl.String(index='not_analyzed')
    password_hash = dsl.String(index='not_analyzed')

    auth_tokens = dsl.Object(
        multi=True,
        properties={
            'account': dsl.String(index='not_analyzed'),
            'token': dsl.String(index='not_analyzed')
        }
    )

    @staticmethod
    def _calculate_hash(password):
        return hexlify(
            pbkdf2_hmac(
                app.config['PASSWORD_HASH_ALGO'],
                password,
                app.config['PASSWORD_SALT'],
                app.config['PASSWORD_ROUNDS'],
            )
        )

    def set_password(self, password):
        self.password_hash = self._calculate_hash(password)

    def check_password(self, password):
        return self.password_hash == self._calculate_hash(password)
