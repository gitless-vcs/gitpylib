# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for dealing with Git files."""


import os.path

import common


SUCCESS = 1
FILE_NOT_FOUND = 2
FILE_NOT_FOUND_AT_CP = 3


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

  fp = common.fix_case(fp)

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

  fp = common.fix_case(fp)

  # "git reset" currently returns 0 (if successful) while "git reset
  # $pathspec" returns 0 iff the index matches HEAD after resetting (on all
  # paths, not just those matching $pathspec). See
  # http://comments.gmane.org/gmane.comp.version-control.git/211242.
  # So, we need to ignore the return code (unfortunately) and hope that it
  # works.
  common.git_call('reset %s HEAD' % fp)
  return SUCCESS


def show(fp, cp):
  """Gets the contents of file fp at commit cp.
 
  Args:
    fp: the file to get its contents from.
    cp: the commit point.

  Returns:
    a pair (status, out) where status is one of FILE_NOT_FOUND_AT_CP or SUCCESS
    and out is the content of fp at cp.
  """
  fp = common.fix_case(fp)

  ok, out, unused_err = common.git_call('show %s:%s' % (cp, fp))

  if not ok:
    return (FILE_NOT_FOUND_AT_CP, None)

  return (SUCCESS, out)


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

  fp = common.fix_case(fp)

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

  fp = common.fix_case(fp)

  common.safe_git_call('update-index --no-assume-unchanged %s' % fp)
  return SUCCESS


def diff(fp):
  """Compute the diff of the given file with its last committed version.

  Args:
    fp: the path of the file to diff (e.g., 'paper.tex').

  Returns:
    A pair (result, out) where result is one of:
      - SUCCESS: the operation completed successfully or
      - FILE_NOT_FOUND: the given file doesn't exist;
    and out is the output of the diff command.
  """
  if not os.path.exists(fp):
    return (FILE_NOT_FOUND, '')

  # Diff only works with real-case :S
  fp = common.real_case(fp)

  out, unused_err = common.safe_git_call('diff %s' % fp)
  return (SUCCESS, out)


def staged_diff(fp):
  """Compute the diff of staged version vs last committed version.

  Args:
    fp: the path of the file to diff (e.g., 'paper.tex').

  Returns:
    A pair (result, out) where result is one of:
      - SUCCESS: the operation completed successfully or
      - FILE_NOT_FOUND: the given file doesn't exist;
    and out is the output of the diff command.
  """
  if not os.path.exists(fp):
    return (FILE_NOT_FOUND, '')

  fp = common.fix_case(fp)

  out, unused_err = common.safe_git_call('diff --cached %s' % fp)
  return (SUCCESS, out)
