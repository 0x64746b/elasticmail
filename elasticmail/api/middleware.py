# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import httplib

from flask import abort, current_app as app, g, request

from elasticmail.gui.models import User
from .models import mail_index


def authenticate_by_token():
    """Authenticate a request by the presented auth token."""
    auth_header = request.headers.get('Authorization', '').split()

    if len(auth_header) == 2 and auth_header[0] == 'Bearer':
        users = User.search(index=mail_index._name).filter('term', **{'auth_tokens.token': auth_header[1]}).execute()

        if users.hits.total == 0:
            abort(httplib.UNAUTHORIZED)
        elif users.hits.total == 1:
            g.user = users.hits[0]
            g.authenticated_account = next(
                authenticator.account for authenticator in g.user.auth_tokens
                if authenticator.token==auth_header[1]
            )
        else:
            app.logger.error(
                'Found {} users with token {}: {}'.format(
                    users.hits.total,
                    auth_header[1],
                    [user.to_dict() for user in users.hits]
                )
            )
            abort(httplib.INTERNAL_SERVER_ERROR)
    else:
        abort(httplib.UNAUTHORIZED)
