# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from email import message_from_string
import httplib

from flask import Blueprint, g, request

from .models import Mail, mail_index


api = Blueprint('api', __name__)


@api.route('/mail', methods=['POST'])
def index_mail():
    print('incoming mail from %s via %s' % (g.user.user_name, g.authenticated_account))

    mail = message_from_string(request.data)

    doc = Mail(
        owner='dtk@execvebin.sh',
        headers=dict(mail.items())
    )

    for part in mail.walk():
        if part.get_content_maintype() == 'text':
	    #FIXME: This flattens the tree, so last write wins
            doc.parts[part.get_content_subtype()] = part.get_payload()

    doc.meta.id = mail['Message-ID']
    created = doc.save(index=mail_index._name)

    return '', httplib.NO_CONTENT if created else httplib.CONFLICT
