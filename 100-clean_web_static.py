#!/usr/bin/python3
"""100-clean_web_static module

A Fabric script has extra functionality that cleans deployments
"""
from fabric.api import env, local, run

env.hosts = ["54.237.44.150", "100.25.0.186"]


def do_clean(number=0):
    """cleans outdated archives

    Args:
        number (int, optional): number of versions to keep. Defaults to 0.
    """
    number = int(number)
    number = number if number >= 2 else 1

    try:
        local(
            "ls -t /versions | tail -n +{} | xargs rm -rf".format(number + 1)
        )

        remote_path = "/data/web_static/releases"
        run(
            "ls -t {} | tail -n +{} | xargs rm -rf".format(
                remote_path, number + 1
            )
        )
    except Exception:
        pass
