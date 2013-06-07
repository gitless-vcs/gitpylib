"""Module for dealing with Git files."""


__author__ = "Santiago Perez De Rosso (sperezde@csail.mit.edu)"


import os.path

import common


SUCCESS = 1
FILE_NOT_FOUND = 2


def stage(fp):
  """Stages the given file.
  
  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed successfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  if not os.path.exists(fp):
    return FILE_NOT_FOUND

  common.safe_git_call('add %s' % fp)
  return SUCCESS


def unstage(fp):
  """Unstages the given file.
  
  Args:
    fp: the path of the file to unstage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed successfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  if not os.path.exists(fp):
    return FILE_NOT_FOUND

  # "git reset" currently returns 0 (if successful) while "git reset
  # $pathspec" returns 0 iff the index matches HEAD after resetting (on all
  # paths, not just those matching $pathspec). See
  # http://comments.gmane.org/gmane.comp.version-control.git/211242.
  # So, we need to ignore the return code (unfortunately) and hope that it
  # works.
  common.git_call('reset HEAD %s' % fp)
  return SUCCESS


def assume_unchanged(fp):
  """Marks the given file as assumed-unchanged.

  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed successfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  if not os.path.exists(fp):
    return FILE_NOT_FOUND

  common.safe_git_call('update-index --assume-unchanged %s' % fp)
  return SUCCESS


def not_assume_unchanged(fp):
  """Unmarks the given assumed-unchanged file.

  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed successfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  if not os.path.exists(fp):
    return FILE_NOT_FOUND

  common.safe_git_call('update-index --no-assume-unchanged %s' % fp)
  return SUCCESS
