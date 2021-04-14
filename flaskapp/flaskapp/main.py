#!/bin/env python
import time
import random
import threading
import subprocess
import select
from datetime import datetime

from flask import Flask, Response, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask.logging import default_handler

from plotting_example import create_plot, get_new_data

import logging
logger = logging.getLogger()

app = Flask(__name__)
Bootstrap(app)

data_save = []

def data_gen():
    """A function to simply generate log data.
    """
    while True:
        logger.info("In data_gen thread. {} {}".format(datetime.now(), random.randint(0, 2**32)))
        time.sleep(1)


@app.route('/')
@app.route('/home')
def home():
    logger.info("In home {}".format(datetime.now()))
    return render_template("home.html", content="Welcome to home")


@app.route('/test')
def test():
    logger.info("In test {}".format(datetime.now()))
    return render_template("home.html", content="Welcome to test")


@app.route('/plot')
def plot():
    global data_save
    logger.info("In plot {}".format(datetime.now()))
    data_save = []
    bar, scatter, dyn = create_plot()
    return render_template("plotting.html", bar=bar, scatter=scatter, dyn=dyn)


@app.route('/get_new_plot_data')
def get_new_plot_data():
    global data_save
    return get_new_data(data_save)


@app.route('/stream')
def stream():
    # The trick with streaming data is that the template is rendered once, and
    # javascript must request data updates.
    logger.info("In stream {}".format(datetime.now()))
    return render_template("stream.html")


@app.route('/get_data')
def get_data():
    logger.info("In get_data {}".format(datetime.now()))

    def generate():

        f = subprocess.Popen(['tail', '-F', 'flask.log'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)

        # Note that the strings yielded below accumulate in the javascript in
        # the browser. Even though we are only yielding a line at a time, these
        # all build up in the browser. Just something I didn't expect.
        while True:
            if p.poll(1):
                yield f.stdout.readline()
            time.sleep(.5)

    return app.response_class(generate(), mimetype="text/plain")


def main():
    logging.basicConfig(
        format='[%(levelname)s: %(module)s %(message)s',
        filename='flask.log',
        filemode='w',
        level=logging.DEBUG)

    #fh = logging.FileHandler()
    #fh.setLevel(logging.DEBUG)
    #logger.addHandler(fh)
    #logger.addHandler(default_handler)

    th = threading.Thread(target=data_gen)
    th.start()

    app.run(debug=True)

if __name__ == "__main__":
    main()
