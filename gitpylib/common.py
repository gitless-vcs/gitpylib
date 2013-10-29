# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Common methods used accross the gitpylib."""


import os
import subprocess


# Detect if FS is case-sensitive.
import tempfile

tmp_handle, tmp_path = tempfile.mkstemp()
with tempfile.NamedTemporaryFile() as f:
  FS_CASE_SENSITIVE = not os.path.exists(f.name.upper())


def safe_git_call(cmd):
  ok, out, err = git_call(cmd)
  if ok:
    return out, err
  raise Exception('%s failed: out is %s, err is %s' % (cmd, out, err))


def git_call(cmd):
  p = subprocess.Popen(
      'git %s' % cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
      shell=True)
  out, err = p.communicate()
  return p.returncode == 0, out, err


def real_case(fp):
  """Returns the same file path with its real casing.

  Args:
    fp: the file path to get the real-casing for. It should correspond to an
        existing file.

  Returns:
    the same file path with its real casing.
  """
  if FS_CASE_SENSITIVE:
    return fp

  cdir = os.getcwd()
  ret = []
  for p in fp.split('/'):
    found = False
    for f in os.listdir(cdir):
      if f.lower() == p.lower():
        cdir = os.path.join(cdir, p)
        ret.append(f)
        found = True
        break
    if not found:
      # TODO(sperezde): fix this hack
      # raise Exception("Invalid file %s: the file doesn't exist" % fp)
      # Temp hack until I figure out how to deal with filenames with special
      # characters.
      return fp
  return os.path.join(*ret)


def git_dir():
  """Gets the path to the .git directory

  Returns:
    the absolute path to the git directory or None if the current working
    directory is not a Git repository.
  """
  cd = os.getcwd()
  ret = os.path.join(cd, '.git')
  while cd != '/':  # TODO(sperezde): windows support
    if os.path.isdir(ret):
      return ret
    cd = os.path.dirname(cd)
    ret = os.path.join(cd, '.git')
  return None


def repo_dir():
  """Gets the full path to the Git repo."""
  return git_dir()[:-4]  # Strip "/.git"


def remove_dups(list, key):
  """Returns a new list without duplicates.

  Given two elements e1, e2 from list, e1 is considered to be a duplicate of e2
  if key(e1) == key(e2).

  Args:
    list: the list to read from.
    key: a function that receives an element from list and returns its key.

  Returns:
    a new list without duplicates.
  """
  keys = set()
  ret = []
  for a in list:
    k_a = key(a)
    if k_a not in keys:
      keys.add(k_a)
      ret.append(a)
  return ret
