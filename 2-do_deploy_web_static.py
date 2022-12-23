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
        if not path.exists(archive_path):
            return False

        archive_name_w_ext = path.basename(archive_path)
        archive_name = archive_name_w_ext.split(".")[0]

        put(archive_path, "/tmp/")
        run(
            "mkdir -p mkdir -p /data/web_static/releases/{}/".format(
                archive_name)
        )

        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_name_w_ext, archive_name)
        )

        run("rm /tmp/{}".format(archive_name_w_ext))

        run(
            "mv /data/web_static/releases/{}/web_static/*\
                /data/web_static/releases/{}/".format(
                archive_name, archive_name)
        )

        run(
            "rm -rf /data/web_static/releases/{}/web_static/".format(
                archive_name)
        )

        link = "/data/web_static/current"
        run("rm -rf {}".format(link))
        run(
            "ln -s /data/web_static/releases/{}/ {}".format(archive_name, link)
        )
        print("New version deployed!")
        return True
    except Exception:
        return False
