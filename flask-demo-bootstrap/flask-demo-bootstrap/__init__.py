import os

from flask import Flask
from flask_bootstrap import Bootstrap

from rich.logging import RichHandler

import logging
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
sfmt = logging.Formatter('[%(levelname)s: %(module)s]: %(message)s')
sh = RichHandler(rich_tracebacks=True)
sh.setFormatter(sfmt)
sh.setLevel(logging.INFO)

fh = logging.FileHandler('flask.log', mode='w')
ffmt = logging.Formatter('[%(levelname)s: %(module)s]: %(message)s')
fh.setFormatter(ffmt)
fh.setLevel(logging.DEBUG)

# Disable flask logging.
log = logging.getLogger('werkzeug')
log.disabled = True

logger.addHandler(sh)
logger.addHandler(fh)

# Extensions
bootstrap = Bootstrap()


def create_app(test_config=None):
    """Creates and configures an application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # default secret key that should be overridden by the instance config.
        SECRET_KEY='dev',
        BOOTSTRAP_SERVE_LOCAL=True,
    )

    # Init extensions.
    bootstrap.init_app(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    # Make sure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create basic routes.

    # Register blueprints.
    from . import main

    app.register_blueprint(main.bp)

    return app
