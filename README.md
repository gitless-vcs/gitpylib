gitpylib
=========

[![PyPI version](https://badge.fury.io/py/gitpylib.svg)](
  http://badge.fury.io/py/gitpylib)

Python library for Git.

gitpylib is a lightweight wrapper of the `git` command.

**As of 02/2015 gitpylib is no longer mantained. If you are looking to interact
with git repositories from Python you can use [subprocess](https://docs.python.org/2/library/subprocess.html)
or [sh](http://amoffat.github.io/sh/) to call to `git` directly
or use [pygit2](http://www.pygit2.org/), [dulwich](https://www.samba.org/~jelmer/dulwich/)
or [gitpython](https://gitpython.readthedocs.org/en/stable/). gitpylib used to sit somewhere in the middle
between these two alternatives.**

Install
-------

Via `pip` (the Python Package Manager):

    $> pip install gitless
