# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.


import subprocess


def log(include_diffs=False):
  # The pipe to less shouldn't be here. TODO: fix.
  subprocess.call(
      'git log {0} | less'.format('-p' if include_diffs else ''), shell=True)
