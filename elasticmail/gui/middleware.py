# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import httplib

from flask import redirect, request, session, url_for

from elasticmail.gui.models import User

 
UNAUTHENTICATED_VIEWS = [
    'gui.login',
]


def authenticate_by_cookie():
    """Authenticate a request by the presented cookie."""

    if request.path in [url_for(view) for view in UNAUTHENTICATED_VIEWS]:
        return

    if not 'user' in session:
        return redirect(url_for('gui.login', next=request.path))
