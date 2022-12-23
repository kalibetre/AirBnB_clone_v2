#!/usr/bin/python3
"""2-do_deploy_web_static module

A Fabric script that deploys an archive to a web server
"""
from os import path

from fabric import task

web_hosts = ["ubuntu@54.237.44.150", "ubuntu@100.25.0.186"]


@task(hosts=web_hosts)
def do_deploy(ctx, archive_path):
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

        ctx.put(archive_path, "/tmp/")
        ctx.run("mkdir -p {}".format(rel_path))
        ctx.run("tar -xzf {} -C {}".format(tmp_path, rel_path))
        ctx.run("rm {}".format(tmp_path))
        ctx.run("mv {}web_static/* {}".format(rel_path, rel_path))
        ctx.run("rm -rf {}web_static/".format(rel_path))

        link = "/data/web_static/current"
        ctx.run("rm -rf {}".format(link))
        ctx.run("ln -s {} {}".format(rel_path, link))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
