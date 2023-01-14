#!/usr/bin/python3
"""2-c_route module

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


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """c_text route

    Returns:
        string: simple message c followed by the text given
    """
    text = text.replace("_", "")
    return f"c {text}"


if __name__ == "__main__":
    app.run()
