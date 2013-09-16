# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Hook module for running Git hooks."""


import collections
import os
import subprocess

import common


def pre_commit():
  """Runs the pre-commit hook."""
  return _hook_call('pre-commit')


def _hook_call(hook_name):
  HookCall = collections.namedtuple('hook_call', ['ok', 'out', 'err'])
  hook_path = '{}/hooks/{}'.format(common.git_dir(), hook_name)
  if not os.path.exists(hook_path):
    return HookCall(True, '', '')
  p = subprocess.Popen(
      hook_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = p.communicate()
  return HookCall(p.returncode == 0, out, err)
