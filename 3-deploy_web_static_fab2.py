#!/usr/bin/python3
"""3-deploy_web_static module

A Fabric script that deploys packs and deploys web static page
"""
from datetime import datetime
from os import path

import invoke
from fabric import task

web_hosts = ["ubuntu@54.237.44.150", "ubuntu@100.25.0.186"]


@task
def do_pack(ctx):
    """packs a folder to a .tgz archive

    Returns:
        str: file path
    """
    try:
        invoke.run('mkdir -p versions')
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(time)
        invoke.run("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None


@task(hosts=web_hosts)
def do_deploy(ctx, archive_path):
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

        ctx.put(archive_path, "/tmp/")
        ctx.run("mkdir -p {}".format(rel_path))
        ctx.run("tar -xzf {} -C {}".format(tmp_path, rel_path))
        ctx.run("rm {}".format(tmp_path))
        ctx.run("mv {}web_static/* {}".format(rel_path, rel_path))
        ctx.run("rm -rf {}web_static".format(rel_path))

        link = "/data/web_static/current"
        ctx.run("rm -rf {}".format(link))
        ctx.run("ln -s {} {}".format(rel_path, link))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


@task(hosts=web_hosts)
def deploy(ctx):
    """packs and deploys a web static to web servers

    Returns:
        bool: True if it succeeded else False
    """
    archive_path = do_pack(ctx)
    if archive_path is None:
        return False
    return do_deploy(ctx, archive_path)
