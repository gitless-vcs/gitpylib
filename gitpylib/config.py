# gitpylib - a Python library for Git.
# Licensed under GNU GPL v2.

"""Module for dealing with Git config."""


from . import common


def get(var):
  ok, out, _ = common.git_call('config %s' % var)
  return out.strip() if ok else None
