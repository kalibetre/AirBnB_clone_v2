#!/usr/bin/python3
"""1-pack_web_static module

A Fabric script that generates a .tgz archive of all the files in web_static
folder.
"""
from datetime import datetime

from fabric import task


@task
def do_pack(ctx):
    """packs a folder to a .tgz archive

    Returns:
        str: file path
    """
    try:
        ctx.run('mkdir -p versions')
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(time)
        ctx.run("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None
