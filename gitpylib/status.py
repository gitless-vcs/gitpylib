# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for getting the status of the repo."""


import os

import common


SUCCESS = 1
FILE_NOT_FOUND = 2

# Possible status in which a Git file can be in.
TRACKED_UNMODIFIED = 3
TRACKED_MODIFIED = 4
UNTRACKED = 5
ASSUME_UNCHANGED = 6
STAGED = 7
DELETED = 8
DELETED_STAGED = 9  # there are staged changes but then the file was deleted.
# the file is marked as assume-unchanged but it was deleted.
DELETED_ASSUME_UNCHANGED = 10
IN_CONFLICT = 11
IGNORED = 12
IGNORED_STAGED = 13
# the file was a tracked file that was modified after being staged.
MODIFIED_MODIFIED = 14
ADDED_MODIFIED = 15  # file is a new file that was added and then modified.


def of_file(fp):
  """Gets the status of the given file.

  Args:
    fp: the path of the file to status (e.g., 'paper.tex').

  Returns:
    FILE_NOT_FOUND if the given file doesn't exist or one of the possible
    status codes.
  """
  fp = common.real_case(fp)

  ok, out, unused_err = common.git_call(
      'ls-files -tvco --error-unmatch "%s"' % fp)
  if not ok:
    # The file doesn't exist.
    return FILE_NOT_FOUND

  return _status_from_output(out[0], fp)


def au_files():
  """Gets all assumed unchanged files. Paths are relative to the repo dir."""
  out, unused_err = common.safe_git_call(
      'ls-files -v --full-name %s' % common.repo_dir())
  ret = []
  for f_out in common.remove_dups(out.splitlines(), lambda x: x[2:]):
    if f_out[0] == 'h':
      ret.append(f_out[2:])
  return ret


def of_repo():
  """Gets the status of the repo relative to the cwd.

  Yields:
      A pair (status, fp) for each file in the repo. fp is a file path and
      status is the status of the file (TRACKED_UNMODIFIED, TRACKED_MODIFIED,
      UNTRACKED, ASSUME_UNCHANGED, STAGED, etc -- see above).
  """
  unused_ok, out, unused_err = common.git_call('ls-files -tvco')

  for f_out in common.remove_dups(out.splitlines(), lambda x: x[2:]):
    # output is 'S filename' where S is a character representing the status of
    # the file.
    fp = f_out[2:]
    yield (_status_from_output(f_out[0], fp), fp)


def _status_from_output(s, fp):
  if s == '?':
    # We need to see if it is an ignored file.
    out, unused_err = common.safe_git_call('status --porcelain "%s"' % fp)
    if not len(out):
      return IGNORED
    return UNTRACKED
  elif s == 'h':
    return ASSUME_UNCHANGED if os.path.exists(fp) else DELETED_ASSUME_UNCHANGED
  elif s == 'H':
    # We need to use status --porcelain to figure out whether it's deleted,
    # modified or not.
    out, unused_err = common.safe_git_call('status --porcelain "%s"' % fp)
    if not len(out):
      return TRACKED_UNMODIFIED
    # Output is in the form <status> <name>. We are only interested in the
    # status part.
    s = out.strip().split()[0]
    if s == 'M':
      return TRACKED_MODIFIED
    elif s == 'A':
      # It could be ignored and staged.
      out, unused_err = common.safe_git_call(
          'ls-files -ic --exclude-standard "%s"' % fp)
      if len(out):
        return IGNORED_STAGED
      return STAGED
    elif s == 'D':
      return DELETED
    elif s == 'AD':
      return DELETED_STAGED
    elif s == 'MM':
      return MODIFIED_MODIFIED
    elif s == 'AM':
      return ADDED_MODIFIED
    raise Exception(
        "Failed to get status of file %s, out %s, status %s" % (fp, out, s))
  elif s == 'M':
    return IN_CONFLICT

  raise Exception("Failed to get status of file %s, status %s" % (fp, s))
