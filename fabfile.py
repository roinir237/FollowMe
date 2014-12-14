from __future__ import with_statement
from fabric.api import env, abort, settings, run, cd

env.hosts = ['root@karmapleaseapp.com']

def deploy():
    code_dir = '/srv/www/twitterbot'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:roinir237/FollowMe.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        if run("test -d requirements.txt").failed:
            abort("No requirements.txt file found.")
        run("pip install -r requirements.txt")