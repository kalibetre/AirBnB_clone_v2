#!/usr/bin/python3
"""3-deploy_web_static module

A Fabric script that deploys packs and deploys web static page
"""
from datetime import datetime
from os import path

from fabric.api import env, local, put, run

env.hosts = ["54.237.44.150", "100.25.0.186"]


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


def do_deploy(archive_path):
    """deploys a web_static archive to a web server

    Args:
        archive_path (str): the path of the archive

    Returns:
        bool: True if success else False
    """
    try:
        archive_name_w_ext = path.basename(archive_path)
        archive_name = archive_name_w_ext.split(".")[0]

        rel_path = "/data/web_static/releases/{}/".format(archive_name)
        tmp_path = "/tmp/{}".format(archive_name_w_ext)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(rel_path))
        run("tar -xzf {} -C {}".format(tmp_path, rel_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(rel_path, rel_path))
        run("rm -rf {}web_static/".format(rel_path))

        link = "/data/web_static/current"
        run("rm -rf {}".format(link))
        run("ln -s {} {}".format(rel_path, link))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """packs and deploys a web static to web servers

    Returns:
        bool: True if it succeeded else False
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
