#!/usr/bin/python3
"""0-hello_route module

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


if __name__ == "__main__":
    app.run()
