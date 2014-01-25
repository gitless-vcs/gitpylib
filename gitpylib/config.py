# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for dealing with Git config."""


from . import common


def get(var):
  ok, out, unused_err = common.git_call('config %s' % var)
  return out.strip() if ok else None
