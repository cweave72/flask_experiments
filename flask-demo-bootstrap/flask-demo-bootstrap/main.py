from flask import Response, render_template
from flask import Blueprint

import logging
logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)


@bp.route('/')
@bp.route('/home')
def home():
    logger.info("In home")
    return render_template('layout.html', title='main page')


@bp.route('/simple')
def simple():
    logger.info("In simple")
    return render_template('simple_sidebar.html', title='simple-sidebar')
