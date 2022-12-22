#!/usr/bin/python3
"""2-do_deploy_web_static module

A Fabric script that deploys an archive to a web server
"""
from os import path

from fabric.api import env, put, run

env.hosts = ["54.237.44.150", "100.25.0.186"]


def do_deploy(archive_path):
    """deploys a web_static archive to a web server

    Args:
        archive_path (str): the path of the archive

    Returns:
        bool: True if success else False
    """
    try:
        if not path.isfile(archive_path):
            return False

        archive_name_w_ext = archive_path.split("/")[-1]
        archive_name = archive_name_w_ext.split(".")[0]

        rel_path = "/data/web_static/releases/{}/".format(archive_name)
        tmp_path = "/tmp/{}".format(archive_name_w_ext)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(rel_path))
        run("tar -xzf {} -C {}".format(tmp_path, rel_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(rel_path, rel_path))
        run("rm -rf {}web_static".format(rel_path))

        link = "/data/web_static/current"
        run("rm -rf {}".format(link))
        run("ln -s {} {}".format(rel_path, link))
        print("New version deployed!")
        return True
    except Exception:
        return False
