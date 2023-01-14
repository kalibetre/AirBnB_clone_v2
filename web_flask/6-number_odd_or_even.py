#!/usr/bin/python3
"""2-c_route module

Starts a Flask web application
"""
from flask import Flask, render_template

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
    """number that accepts only int numbers

    Args:
        n (int): number

    Returns:
        str: n is number
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """number_template route that accepts only int number and renders
    a template

    Args:
        n (int): number
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """checks if n is even or odd

    Args:
        n (int): number
    """
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run()
