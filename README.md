Description
===========
This is a nasty little python script that was hacked together to copy and convert your bitbucket mercurial repositories to git.  It is very crude with little error checking (I only needed to run it once).

WARNING
-------
Backup your repos first.  This app is not destructive, it does not delete mercurial repos, it renames them. That said you should have a local backup of your repos anyway.

Steps

1. Downloads the mercurial repository.
2. Creates a local git repo
3. Converts the mercurial repository into the newly created local git repo.
4. Renames each mercurial repository to zzz{repo name} HG
5. Creates a new remote (bitbucket) repo with the original repo name
6. Pushes the new git repo up to bitbucket

Usage
=====
`python convert.py`

Requirements
============
* This was tested on OSX.  At the very least you will need an \*nix system to execute the popen calls
* The mercurial python module (pip install mercurial)
* git
* hg

All other dependencies are are packaged with this script they include:

* A modified version of python-bitbucket https://bitbucket.org/jmoiron/python-bitbucket that allows write/create opperations.
* A copy of ht-fast-export http://repo.or.cz/w/fast-export.git

What am I left with?
====================
* Once the script has been run you should have your old hg repo renamed as `zzz{repo name} HG`. I put the zzz prefix so it would move to the bottom of your dashboard (and so I could id repos that have already been converted).
* A new git repo with the name of the original

Other considerations
====================
If you deploy from bitbucket (like I do) you will need to update your local code to point either the new git repo or the new url for the hg repo.

Not everything will be converted to your new git repo.  You will loose issues, wiki pages followers etc.

In case of failure
==================
1. Delete the newly created bitbucket git repo from the web interface (if it was created).
2. Rename the mercurial back to the original name by removing the zzz prefix and HG suffix.

TODO
====
It would be cool to do some command line arguments to only covert a subset of repos etc.  I wanted to convert all my repos so I didn't take the time to do this.

It would also be cool to include a backup script to backup clone all your bitbucket repos locally.  I have one that I use; perhaps I will clean it up and release it.