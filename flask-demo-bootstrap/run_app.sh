#!/bin/bash

export FLASK_ENV=development

VIRTUAL_ENV=.venv

. $VIRTUAL_ENV/bin/activate

if [[ "$?" != 0 ]]; then
    echo Failed to initialize virtual environment.
    return
fi

python -m flask-demo-bootstrap.wsgi
