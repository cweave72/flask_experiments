import os

from flask import Flask
from flask_bootstrap import Bootstrap

import logging
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
sfmt = logging.Formatter('[%(levelname)s: %(module)s]: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(sfmt)
sh.setLevel(logging.INFO)

fh = logging.FileHandler('flask.log', mode='w')
ffmt = logging.Formatter('[%(levelname)s: %(module)s]: %(message)s')
fh.setFormatter(ffmt)
fh.setLevel(logging.DEBUG)

werk = logging.getLogger("werkzeug")
werk.setLevel(logging.INFO)
werk_sh = werk.handlers[0]
wf = logging.Formatter('[%(levelname)s: %(module)s]: %(message)s')
werk_sh.setFormatter(wf)
werk.propagate = False

logger.addHandler(sh)
logger.addHandler(fh)

# Extensions
bootstrap = Bootstrap()

def create_app(test_config=None):
    "Creates and configures an application instance."
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # default secret key that should be overridden by the instance config.
        SECRET_KEY="dev",
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
    from flaskapp import main, plotting_example

    app.register_blueprint(main.bp)
    app.register_blueprint(plotting_example.bp)

    return app
