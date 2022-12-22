#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:"""
from fabric.api import *
import time
from os import path


env.hosts = ['34.74.188.209', '54.226.48.62']
# env.key_filename = "~/.ssh/holberton"
# env.user = "ubuntu"


def do_pack():
    """do_pack
    Returns:
        [string] -- [path to archive]
    """
    localtime = time.localtime(time.time())
    if int(localtime.tm_mon) < 10:
        curmonth = "0{}".format(localtime.tm_mon)
    else:
        curmonth = localtime.tm_mon
    curtime = "{}{}{}{}{}{}".format(localtime.tm_year,
                                    curmonth, localtime.tm_mday,
                                    localtime.tm_hour, localtime.tm_min,
                                    localtime.tm_sec)
    local("mkdir -p versions")
    archivepath = "versions/web_static_{}.tgz".format(curtime)
    archive = local("tar -cvzf {} web_static/".format(archivepath),
                    capture=True)
    if archive:
        return archive
    else:
        return None


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


def deploy():
    """deploy
    Returns:
        [string] -- [path]
    """
    path = do_pack()
    if not path:
        return False
    return do_deploy(path)
