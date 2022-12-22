#!/usr/bin/python3
"""deploy the archive"""
from fabric.api import *
from os import path


env.hosts = ['34.74.188.209', '54.226.48.62']
# env.key_filename = "~/.ssh/holberton"
# env.user = "ubuntu"


def do_deploy(archive_path):
    """do_deploy
    Arguments:
        archive_path {[string]} -- [path to archive file]
    Returns:
        [True or False] -- [True only if successfully deploys archive]
    """
    if not path.exists(archive_path):
        return False
    put(archive_path, "/tmp/")
    name = archive_path.split('/')[-1][:-4]
    run("mkdir -p /data/web_static/releases/{}".format(name))
    run("tar -xzf /tmp/{}.tgz -C ".format(name) +
        "/data/web_static/releases/{}/".format(name))
    run("rm /tmp/{}.tgz".format(name))
    run("mv /data/web_static/releases/{}/web_static/* ".format(name) +
        "/data/web_static/releases/{}/".format(name))
    run("rm -rf /data/web_static/releases/{}/web_static".format(name))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ ".format(name) +
        "/data/web_static/current")
    return True
