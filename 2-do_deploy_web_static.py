#!/usr/bin/python3
"""2-do_deploy_web_static module

A Fabric script that deploys an archive to a web server
"""
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
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(
            archive_path[9:-4]))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_path[9:], archive_path[9:-4]))
        run('rm /tmp/{}'.format(archive_path[9:]))
        path = 'mv /data/web_static/releases/{}/web_static/* \
              /data/web_static/releases/{}/'
        run(path.format(archive_path[9:-4], archive_path[9:-4]))
        run('rm -rf  /data/web_static/releases/{}/web_static/'.format(
            archive_path[9:-4]))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ {}'.format(
            archive_path[9:-4], '/data/web_static/current'))
        return True
    except Exception:
        return False
