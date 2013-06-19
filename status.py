"""Module for getting the status of the repo."""


__author__ = "Santiago Perez De Rosso (sperezde@csail.mit.edu)"


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
DELETED_STAGED = 9 # there are staged changes but then the file was deleted.
# the file is marked as assume-unchanged but it was deleted.
DELETED_ASSUME_UNCHANGED = 10
IN_CONFLICT = 11


def of_file(fp):
  """Gets the status of the given file.

  Args:
    fp: the path of the file to status (e.g., 'paper.tex').

  Returns:
    FILE_NOT_FOUND if the given file doesn't exist or one of the possible
    status codes.
  """
  ok, out, unused_err = common.git_call(
      'ls-files -tvco --error-unmatch %s' % fp)
  if not ok:
    # The file doesn't exist.
    return FILE_NOT_FOUND

  return _status_from_output(out[0], fp)

  
def of_repo():
  """Gets the status of the repo.

  Yields:
      A pair (status, fp) for each file in the repo. fp is a filepath and
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
  if s is '?':
    return UNTRACKED
  elif s is 'h':
    return ASSUME_UNCHANGED if os.path.exists(fp) else DELETED_ASSUME_UNCHANGED
  elif s is 'H':
    # We need to use status --porcelain to figure out whether it's deleted,
    # modified or not.
    out, unused_err = common.safe_git_call('status --porcelain %s' % fp)
    if len(out) is 0:
      return TRACKED_UNMODIFIED
    # Output is in the form <status> <name>. We are only interested in the
    # status part.
    s = out.strip().split()[0]
    if s is 'M':
      return TRACKED_MODIFIED
    elif s is 'A':
      return STAGED
    elif s is 'D':
      return DELETED
    elif s is 'AD':
      return DELETED_STAGED
    raise Exception(
        "Failed to get status of file %s, out %s, status %s" % (fp, out, s))
  elif s is 'M':
    return IN_CONFLICT

  raise Exception("Failed to get status of file %s, status %s" % (fp, s))


