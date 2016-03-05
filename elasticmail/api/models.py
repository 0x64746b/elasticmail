# coding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import elasticsearch_dsl as dsl


mail_index = dsl.Index('elasticmail')


email = dsl.analyzer(
    'email',
    tokenizer='uax_url_email',
    filter = [
        dsl.token_filter(
            'email',
            'pattern_capture',
            preserve_original=True,
            patterns=[
                '([^@]+)',
                '(\\p{L}+)',
                '(\\d+)',
                '@(.+)',
                '([^-@]+)'
            ]
        ),
        'lowercase',
        'unique'
    ]
)


class Mail(dsl.DocType):
    """Model a mail in elasticsearch."""

    owner = dsl.String(index='not_analyzed')
    headers = dsl.Object(
        properties={
            'From': dsl.String(analyzer=email, copy_to="headers.Participants"),
            'To': dsl.String(analyzer=email, copy_to="headers.Participants"),
            'Cc': dsl.String(analyzer=email, copy_to="headers.Participants"),
            'Bcc': dsl.String(analyzer=email, copy_to="headers.Participants"),
            'Subject': dsl.String(),
        }
    )
    parts = dsl.Object()

    class Meta:
        dynamic_templates = dsl.MetaField(
            [
                {
                    'insignificant_headers': {
                        'path_match': 'headers.*',
                        'mapping': {
                            'include_in_all': False,
                        }
                    }
                },
                {
                    'complete_body': {
                        'path_match': 'parts.*',
                        'mapping': {
                            'copy_to': 'body',
                        }
                    }
                }
            ]
        )
