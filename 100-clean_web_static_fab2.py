#!/usr/bin/python3
"""100-clean_web_static module

A Fabric script has extra functionality that cleans deployments
"""
import invoke
from fabric import task

web_hosts = ["ubuntu@54.237.44.150", "ubuntu@100.25.0.186"]


@task(hosts=web_hosts)
def do_clean(ctx, number=0):
    """cleans outdated archives

    Args:
        number (int, optional): number of versions to keep. Defaults to 0.
    """
    number = int(number)
    number = (number if number >= 2 else 1) + 1

    try:
        invoke.run(
            "cd /versions && ls -1t | tail -n +{} | xargs rm -rf".format(
                number)
        )
    except Exception:
        pass

    try:
        remote_path = "/data/web_static/releases"
        ctx.run(
            "cd {} && ls -1t | tail -n +{} | xargs rm -rf".format(
                remote_path, number)
        )
    except Exception:
        pass
