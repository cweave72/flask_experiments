import time
import random
import threading
import subprocess
import select
import logging_tree
import numpy as np
from datetime import datetime

from flask import Flask, Response, render_template, stream_with_context
from flask import Blueprint

import logging
logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)

stream_thrd = None

class DataThread(threading.Thread):
    """Simple thread to create some data.
    """
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):

        logger.info("Creating file {}".format(self.filename))
        f = open(self.filename, 'w')

        line_no = 0
        while True:
            if self.stopped():
                logger.info("Closing file on stop.")
                f.close()
                break

            data = np.random.randint(0, 2**16, size=15)
            line = ["0x{:04X}".format(a) for a in data]
            f.write("line: {:<8}".format(line_no) + " ".join(line) + '\n')
            f.flush()
            line_no += 1

            time.sleep(1)


@bp.route('/')
@bp.route('/home')
def home():
    logger.info("In home {}".format(datetime.now()))
    return render_template("home.html", content="Welcome to home")


@bp.route('/test')
def test():
    logger.info("In test {}".format(datetime.now()))
    return render_template("home.html", content="Welcome to test")


@bp.route('/print_logging')
def print_logging():
    content = logging_tree.format.build_description()
    return render_template("print_logging.html", content=content)


@bp.route('/stream')
def stream():
    global stream_thrd

    # The trick with streaming data is that the template is rendered once, and
    # javascript must request data updates.
    if not stream_thrd:
        logger.info("Creating stream thread.")
        stream_thrd = DataThread("stream_data.txt")
        stream_thrd.start()
    else:
        logger.info("Stream thread already running...stoping")
        stream_thrd.stop()
        stream_thrd.join()

        logger.info("Restaring with fresh file.")
        stream_thrd = DataThread("stream_data.txt")
        stream_thrd.start()

    return render_template("stream.html")


@bp.route('/get_data')
def get_data():
    logger.info("In get_data {}".format(datetime.now()))

    def generate():

        logger.info("Recevied request from web page. Streaming file {}".format(
            stream_thrd.filename))
        f = subprocess.Popen(['tail', '-F', stream_thrd.filename],
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

    return Response(stream_with_context(generate()), mimetype="text/plain")

