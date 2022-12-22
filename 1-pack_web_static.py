#!/usr/bin/python3
"""1-pack_web_static module

A Fabric script that generates a .tgz archive of all the files in web_static
folder.
"""
from datetime import datetime

from fabric.api import local


def do_pack():
    """packs a folder to a .tgz archive

    Returns:
        str: file path
    """
    try:
        local('mkdir -p versions')
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None
