from __future__ import with_statement
from fabric.api import env, abort, settings, run, cd, prefix
from fabric.contrib.files import exists


env.hosts = ['root@karmapleaseapp.com']

def deploy():
    code_dir = '/srv/www/twitterbot'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:roinir237/FollowMe.git %s" % code_dir)
    with prefix('workon twitterbot'):
        with cd(code_dir):
            run("git pull")
            if not exists("requirements.txt"):
                abort("No requirements.txt file found.")
            run("pip install -r requirements.txt")
            run("ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9")
            run("celery -A app.twitterbot worker -B --detach")
