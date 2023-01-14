#!/usr/bin/python3
"""1-hbnb_route module

Starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    """A simple root route

    Returns:
        string: simple message
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb route

    Returns:
        string: simple message
    """
    return "HBNB"


if __name__ == "__main__":
    app.run()
