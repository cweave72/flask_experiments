import time
import json
import plotly
import plotly.graph_objs as graph
from plotly.utils import PlotlyJSONEncoder
from datetime import datetime
import numpy as np

from flask import Blueprint, render_template

import logging
logger = logging.getLogger(__name__)

bp = Blueprint("plots", __name__)

data_save = []

def get_new_data(data_store, numbins=20):
    """This function illustrates how to provide data to a dynamic plotly plot.
    """
    #Generate a new number.
    next_pt = np.random.randn()
    # Add it to the running list.
    data_store.append(next_pt)
    # Compute histogram.
    counts, bins = np.histogram(data_store, bins=numbins)

    # Generate a dict object to be converted to JSON and returned.
    resp = {
        'new_pt': next_pt, 
        'bar': [graph.Bar(x=np.arange(len(counts)), y=counts)]
    }
    return json.dumps(resp, cls=PlotlyJSONEncoder)


def create_plot():
    """ Creates a few simply charts with fixed data.
    """
    N = 100
    x = list(range(N))
    y1 = np.random.randn(N)
    y2 = np.random.randn(N)

    bar_data = [
        graph.Bar(x=x, y=y1)
    ]

    plot_layout = graph.Layout(
        title="my title",
        margin={'l': 10,
                'r': 20,
                'b': 10,
                't': 60,
                'pad': 0},
        yaxis={
            'title': "Y-axis title",
            'automargin': True,
            },
        xaxis={
            'title': "X-axis title",
            'automargin': True,
            },
        paper_bgcolor='yellow',
        plot_bgcolor='red',
        )

    scatter_data = [
        graph.Scatter(x=x, y=y1,
            name='y1',
            line=dict(color='firebrick'),
            mode='lines+markers'),
        graph.Scatter(x=x, y=y2,
            name='y2',
            line=dict(color='blue'),
            mode='lines+markers'),
    ]

    dyn_data = [
        graph.Scatter(y=[np.random.randn()],
            name='randn',
            line=dict(color='blue'),
            mode='lines+markers')
    ]

    layoutJSON = json.dumps(plot_layout, cls=PlotlyJSONEncoder)
    barJSON = json.dumps(bar_data, cls=PlotlyJSONEncoder)
    scatterJSON = json.dumps(scatter_data, cls=PlotlyJSONEncoder)
    dynJSON = json.dumps(dyn_data, cls=PlotlyJSONEncoder)

    return barJSON, scatterJSON, dynJSON, layoutJSON


@bp.route('/plot')
def plot():
    """Create the page template.
    """
    global data_save
    logger.info("In plot {}".format(datetime.now()))
    data_save = []
    bar, scatter, dyn, layout = create_plot()
    return render_template("plotting.html", bar=bar, scatter=scatter, dyn=dyn,
            layout=layout)


@bp.route('/get_new_plot_data')
def get_new_plot_data():
    """This is a callback which is accessed via a javascript fetch() to 
    retrieve new plot data for the dynamic plots.
    """
    global data_save
    return get_new_data(data_save)
