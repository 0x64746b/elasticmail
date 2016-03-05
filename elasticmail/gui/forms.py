# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import elasticsearch_dsl as dsl
from flask_wtf import Form
from wtforms import PasswordField, TextField
from wtforms.fields.html5 import SearchField
from wtforms_components import SelectField

from elasticmail.api.models import Mail, mail_index


class SelectMailField(SelectField):
    main_headers = ('From', 'To', 'Cc', 'Bcc', 'Subject')

    def __init__(self, *args, **kwargs):
        super(SelectMailField, self).__init__(*args, **kwargs)
        self._populate_choices()

    def _populate_choices(self):
        mapping = dsl.Mapping.from_es(mail_index._name, Mail._doc_type.name)
        all_headers = sorted(mapping.to_dict()[mapping.doc_type]['properties']['headers']['properties'].keys())

        self.choices=[
            (
                'Collections', (
                    ('_all', 'Main Fields'),
                    ('body', 'Complete Body')
                )
            ),
            (
                'Main Headers',
                [
                    ('headers.' + header, header)
                    for header in SelectMailField.main_headers
                ]
            ),
            (
                'Other Headers', 
                [
                    ('headers.' + header, header)
                    for header in all_headers
                    if header not in SelectMailField.main_headers
                    and not header.startswith('X-')
                ]
            ),
            (
                'Custom Headers',
                [
                    ('headers.' + header, header)
                    for header in all_headers
                    if header.startswith('X-')
                ]
            )
        ]


class SearchForm(Form):
    search = SearchField('Search for')
    field = SelectMailField('In')


class PasswordForm(Form):
    current = PasswordField('Current password')
    new = PasswordField('New password')
    new_confirm = PasswordField('Confirmation')


class LoginForm(Form):
    user_name = TextField()
    password = PasswordField()
