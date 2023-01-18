#!/usr/bin/python3
"""A Flask web application

supported api end points
  - /states : returns list of the states
  - /states/id : returns a state with list of cities
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


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def state(id=None):
    """Returns a state information

    Args:
        id (str): the id of the state

    Returns:
        html: state information n a template format
    """
    states = list(storage.all(State).values())
    if id is None:
        return render_template(
            "9-states.html",
            display="multiple",
            states=states,
        )
    else:
        result = list(filter(lambda x: x.id == id, states))
        state = result[0] if len(result) > 0 else False
        return render_template("9-states.html", display="single", state=state)


if __name__ == "__main__":
    storage.reload()
    app.run("0.0.0.0", 5000)
