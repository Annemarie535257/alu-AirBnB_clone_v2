#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, put, run, local
from os.path import exists

env.hosts = ['54.234.251.73', '54.167.82.129']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"

def do_deploy(archive_path):
    """Function to distribute an archive to your web servers"""
    if not exists(archive_path):
        print("Archive path does not exist.")
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        print(f"Uploading {archive_path} to /tmp/")
        result = put(archive_path, "/tmp/")
        if result.failed:
            print("Failed to upload the archive")
            return False
        print(f"Creating directory {path_name}/")
        run("mkdir -p {}/".format(path_name))
        print(f"Extracting {file_name} to {path_name}/")
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
        print(f"Removing {file_name} from /tmp/")
        run("rm /tmp/{}".format(file_name))
        print(f"Moving files from {path_name}/web_static to {path_name}")
        run("mv {}/web_static/* {}".format(path_name, path_name))
        print(f"Removing {path_name}/web_static")
        run("rm -rf {}/web_static".format(path_name))
        print(f"Removing old symbolic link /data/web_static/current")
        run('rm -rf /data/web_static/current')
        print(f"Creating new symbolic link /data/web_static/current -> {path_name}")
        run('ln -s {}/ /data/web_static/current'.format(path_name))
        print("Deployment successful.")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
