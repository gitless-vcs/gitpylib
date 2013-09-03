# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.


import common


def clone(repo):
  common.safe_git_call('clone %s .' % repo)


def init():
  common.safe_git_call('init')
