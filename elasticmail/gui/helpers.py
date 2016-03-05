# coding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import quopri
import re

from jinja2 import evalcontextfilter, Markup, escape
from lxml.html.clean import clean_html


paragraphs = re.compile(r'(?:\n){2,}')


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = ''.join(
        '<p>%s</p>' % p.replace('\n', Markup('<br />'))
        for p in paragraphs.split(escape('\n'.join(value.splitlines())))
    )
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@evalcontextfilter
def scrub_html(eval_ctx, value):
    return str.decode(clean_html(quopri.decodestring(value)), 'utf-8')
