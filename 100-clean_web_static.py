#!/usr/bin/python3
"""100-clean_web_static module

A Fabric script has extra functionality that cleans deployments
"""
from fabric.api import cd, env, lcd, local, run

env.hosts = ["54.237.44.150", "100.25.0.186"]


def do_clean(number=0):
    """cleans outdated archives

    Args:
        number (int, optional): number of versions to keep. Defaults to 0.
    """
    number = int(number)
    number = (number if number >= 2 else 1) + 1

    try:
        with lcd("versions"):
            local("ls -1t | tail -n +{} | xargs rm -rf".format(number))

        with cd("/data/web_static/releases"):
            run("ls -1t | tail -n +{} | xargs rm -rf".format(number))
    except Exception:
        pass
