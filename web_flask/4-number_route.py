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

    Args:
        text (str): text to be appended

    Returns:
        str: c followed by the given text
    """
    return "C {}".format(text.replace("_", " "))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    """python_text route with and without parameter

    Args:
        text (str): text to be appended defaults to 'is cool'

    Returns:
        str: c followed by the given text
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """python_text route with and without parameter

    Args:
        n (int): number

    Returns:
        str: n is number
    """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run()
