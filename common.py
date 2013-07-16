# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Common methods used accross the gitpylib."""


import os
import subprocess


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


def fix_case(fp):
  """Returns the same filepath with the correct casing.

  In UNIX filenames are case-insensitive, meaning that "README" is the same
  thing as "readme" or "ReaDmE" but in Windows these would be different.
  Git commands are case-sensitive but the gitpylib is case-insensitive if
  executing in UNIX and case-sensitive in Windows thus making its behaviour
  consistent with the OS. This method is used to normalize the filepath before
  passing it to a Git command.

  Args:
    fp: the filepath to case-correct. It should correspond to an existing file.

  Returns:
    The same filepath with the correct casing (OS-dependent).
  """
  # TODO(sperezde): if windows => do nothing
  return fp.lower()


def real_case(fp):
  """Returns the same filepath with its real casing.

  Args:
    fp: the filepath to get the real-casing for. It should correspond to an
        existing file.

  Returns:
    The same filepath with it's real casing.
  """
  # TODO(sperezde): if windows => do nothing
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
    The absolute path to the git directory or None if the current working
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


def remove_dups(list, key):
  """Returns a new list without duplicates."""
  keys = set()
  ret = []
  for a in list:
    k_a = key(a)
    if k_a not in keys:
      keys.add(k_a)
      ret.append(a)
  return ret
