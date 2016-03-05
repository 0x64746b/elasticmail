# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import logging
import uuid

import elasticsearch_dsl as dsl
from flask import Flask
from flask_appconfig import AppConfig

from .default_config import CONFIG_DIR


def create_app(config_file=None):
    """Create and configure an ElasticMail instance."""

    # Create the WSGI callable
    app = Flask(
    	'elasticmail',
	instance_path=CONFIG_DIR,
        instance_relative_config=True
    )

    # Load configuration
    AppConfig(app, config_file)

    # Session key
    app.secret_key = str(uuid.uuid4())

    # Register and setup components
    from .api.views import api
    from .gui.views import gui

    from .api.middleware import authenticate_by_token
    from .gui.middleware import authenticate_by_cookie
    api.before_request(authenticate_by_token)
    gui.before_request(authenticate_by_cookie)

    app.register_blueprint(api, url_prefix='/api') 
    app.register_blueprint(gui)

    # Connect to ES
    # https://elasticsearch-py.readthedocs.org/en/master/#persistent-connections
    es_host = app.config['ELASTICSEARCH_HOST']
    if es_host:
	app.es = dsl.connections.connections.create_connection(hosts=[es_host])

    # Register template filter
    from .gui.helpers import nl2br, scrub_html
    app.jinja_env.filters['nl2br'] = nl2br
    app.jinja_env.filters['html_mail'] = scrub_html

    # Configure logging
    if not app.debug:
        file_handler = logging.FileHandler('logs/access.log')
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)
    else:
        default_handler = app.logger.handlers[0]
        default_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(module)s [%(levelname)s]: %(message)s'
            )
        )
        default_handler.setLevel(app.config['LOG_LEVEL'])

    return app
