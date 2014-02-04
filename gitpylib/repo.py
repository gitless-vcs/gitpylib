# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.


from . import common


def clone(repo):
  """Returns True if the clone succeeded, False if otherwise."""
  return common.git_call('clone %s .' % repo)[0]


def init():
  common.safe_git_call('init')
