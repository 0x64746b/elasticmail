#!/usr/bin/env python
# coding: utf-8


"""Run management commands."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import importlib
import inspect
import pkgutil

import elasticsearch_dsl as dsl
from flask import current_app
from flask.ext.script import Manager, Server, Shell

from elasticmail import create_app
from elasticmail.gui.commands.create_user import UserCreator


def _build_shell_context():
    """Make symbols automagically available in shell."""
    context = dict()

    context['app'] = current_app
    context['dsl'] = dsl

    # auto import models
    for _, name, is_pkg in pkgutil.walk_packages('.'):
        if not is_pkg and 'models' in name:
            module = importlib.import_module(name)
            for member in inspect.getmembers(module, inspect.isclass):
                context[member[0]] = member[1]

    return context


manager = Manager(create_app)
manager.add_option(
    '-c',
    '--config',
    metavar='FILE',
    dest='config_file',
    default='development.py',
    help='the config file to be loaded [default: %(default)s]'
)

manager.add_command('runserver', Server(use_debugger=True, use_reloader=True))
manager.add_command('shell', Shell(make_context=_build_shell_context))
manager.add_command('create_user', UserCreator())


if __name__ == '__main__':
    try:
        manager.run()
    except KeyboardInterrupt:
        sys.exit('Command has been interrupted')
