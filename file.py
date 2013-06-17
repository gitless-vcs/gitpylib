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
  return reset(fp, 'HEAD')


def reset(fp, cp):
  """Resets the given file to the given commit point.
  
  Args:
    fp: the path of the file to reset.
    cp: the commit point to reset the file to.

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
  common.git_call('reset %s %s' % (cp, fp))
  return SUCCESS


def show(fp, cp, dst):
  fp = common.fix_case(fp)

  common.safe_git_call('show %s:%s >%s' % (cp, fp, dst))


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

  fp = common.fix_case(fp)

  out, unused_err = common.safe_git_call('diff %s' % fp)
  return (SUCCESS, out)
