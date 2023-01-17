#!/usr/bin/python3
"""A Flask web application
"""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ Cleanup Db Session
    """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Lists states

    Returns:
        string: simple message
    """
    states = list(storage.all(State).values())
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    storage.reload()
    app.run()
