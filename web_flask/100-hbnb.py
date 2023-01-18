#!/usr/bin/python3
"""A Flask web application

supported api end points
  - /states : returns list of the states
  - /states/id : returns a state with list of cities
"""
from flask import Flask, render_template

from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ Cleanup Db Session
    """
    storage.close()


@app.route("/hbnb")
def hbnb_filters():
    states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    places = list(storage.all(Place).values())
    return render_template(
        "100-hbnb.html",
        states=states,
        amenities=amenities,
        places=places,
    )


if __name__ == "__main__":
    storage.reload()
    app.run("0.0.0.0", 5000)
