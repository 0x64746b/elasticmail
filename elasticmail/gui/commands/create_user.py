# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from getpass import getpass
import sys

from flask.ext.script import Command, Option

from elasticmail.api.models import mail_index
from elasticmail.gui.models import User


class UserCreator(Command):
    """Create a new user."""

    option_list = (
        Option('--user-name', '-u'),
    )


    def run(self, user_name):
        users = User.search(
            index=mail_index._name
        ).extra(
            size=0,
            terminate_after=1,
        ).filter(
            'term',
            user_name=user_name,
        ).execute()

        if users.hits.total == 0:
            password = getpass()

            user = User(user_name=user_name)
            user.set_password(password)
            
            user.save(index=mail_index._name)
        else:
            exit('There already is a user with the name {}.'.format(user_name))
