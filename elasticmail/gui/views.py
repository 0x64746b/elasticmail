# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import httplib
import json

from flask import (
    abort,
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from elasticmail.api.models import Mail, mail_index
from .forms import LoginForm, PasswordForm, SearchForm
from .models import User


gui = Blueprint(
    'gui',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/gui',
)


@gui.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        users = User.search(
            index=mail_index._name
        ).filter(
            'term',
            user_name=form.user_name.data
        ).execute()

        if users.hits.total == 0:
            flash('Invalid username or password', 'danger')
        if users.hits.total == 1:
            user = users.hits[0]
            if user.check_password(form.password.data):
                session['user'] = user.to_dict()
		print(request.args)
                return redirect(request.args.get('next', url_for('gui.search')))
            else:
                flash('Invalid username or password', 'danger')
        else:
            app.logger.error(
                'Found {} users with name {}: {}'.format(
                    users.hits.total,
                    user_name,
                    [user.to_dict() for user in users.hits]
                )
            )
            abort()

    return render_template('login.html', form=form)


@gui.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        matches = Mail.search(
            index=mail_index._name
        ).query(
            'match',
            **{form.field.data: form.search.data}
        ).execute()

	if matches.hits.total:
	    return render_template('results.html', hits=matches.hits)
	else:
	    flash('No matching mails found', 'warning')

    return render_template('search.html', form=form)


@gui.route('/settings', methods=['GET', 'POST'])
def settings():
    pass_form = PasswordForm()

    return render_template(
        'settings.html',
        name=session['user']['user_name'],
        tokens=session['user']['auth_tokens'],
        pass_form=pass_form,
    )


@gui.route('/logout', methods=['GET'])
def logout():
    session.pop('user')
    return redirect(url_for('gui.login'))
