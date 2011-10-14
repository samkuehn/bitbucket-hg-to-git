#!/usr/bin/env python
import bitbucket
import os
from getpass import getpass
import logging
import logging.config
import time

logging.config.fileConfig('logging.conf')
log = logging.getLogger('bitbucket-hg-to-git')

def main():
    username = raw_input('Enter your bitbucket username: ')
    password = getpass(prompt='Enter your bitbucket password: ')
    bb = bitbucket.BitBucket(username, password)
    print bb
    try:
        user = bb.user(username)
    except TypeError:
        print('Looks like you probably typed in the wrong username.')
    repos = user.repositories()
    if not repos:
        print('No repos found. Perhaps you typed in the wrong password.')
        exit(0)
    for repo_data in repos:
        if repo_data.get('scm') != 'hg':
            continue
        if repo_data.get('slug').startswith('zzz'):
            continue
        print 'cloning repo %s...' % repo_data.get('name')
        hg_clone_dir = 'hg-repos/%s' % repo_data.get('slug')
        git_clone_dir = 'git-repos/%s' % repo_data.get('slug')
        os.popen('rm -rf %s' % hg_clone_dir)
        hg_clone_command = "hg clone ssh://hg@bitbucket.org/%s/%s %s" % (username, repo_data.get('slug'), hg_clone_dir)
        os.popen(hg_clone_command)
        print 'creating local git repo...'
        os.popen('rm -rf %s' % git_clone_dir)
        os.popen('mkdir -p %s' % git_clone_dir)
        os.popen('git init %s' % git_clone_dir)
        
        print 'converting hg repo...'
        covert_command = 'cd %s;../../fast-export/hg-fast-export.sh -r ../../%s --force' % (git_clone_dir, hg_clone_dir)
        os.popen(covert_command)
        os.popen('cd %s; git checkout HEAD' % git_clone_dir)
        print 'renaming hg repository...'
        repo = bb.repository(username, repo_data.get('slug'))
        repo.save(dict(name='zzz%s HG' % repo_data.get('name')))
        
        print 'creating new remote repository...'
        bb.create_repo(dict(name=repo_data.get('name'),scm='git',is_private=repo_data.get('is_private'),description=repo_data.get('description')))
        print 'give bitbucket some time to create repo (20 seconds)...'
        time.sleep(20)

        print 'pushing to new git repository...'
        os.popen('cd %s;git remote add origin git@bitbucket.org:%s/%s.git' % (git_clone_dir,username,repo_data.get('slug')))
        os.popen('cd %s;git push origin master' % (git_clone_dir,))
    
if __name__ == "__main__":
    main()