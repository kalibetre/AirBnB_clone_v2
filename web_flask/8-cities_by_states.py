#!/usr/bin/python3
"""A Flask web application

supports the following end points:
    - /states_list : returns list of states
    - /cities_by_states: returns list of cities grouped by state
"""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ Cleanup Db Session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Lists states

    Returns:
        string: list of states in template format
    """
    states = list(storage.all(State).values())
    return render_template("7-states_list.html", states=list(states))


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Lists cities by states

    Returns:
        string: list of cities in a template format
    """
    states = list(storage.all(State).values())
    return render_template("8-cities_by_states.html", states=list(states))


if __name__ == "__main__":
    storage.reload()
    app.run()
