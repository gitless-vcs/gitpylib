# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for getting the status of the repo."""


import os
import re

import common


SUCCESS = 1
FILE_NOT_FOUND = 2

# Possible status in which a Git file can be in.
# (There are actually many more, but these seem to be the only ones relevant
# to Gitless.)
# TODO(sperezde): just have gitpylib's status return the status code and let
# Gitless figure out the rest by itself.
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
# the file was a tracked file that was modified after being staged.
MODIFIED_MODIFIED = 13
ADDED_MODIFIED = 14  # file is a new file that was added and then modified.


def of_file(fp):
  """Gets the status of the given file.

  Args:
    fp: the path of the file to status (e.g., 'paper.tex').

  Returns:
    FILE_NOT_FOUND if the given file doesn't exist or one of the possible
    status codes.
  """
  fp = common.real_case(fp)

  ok, out_ls_files, unused_err = common.git_call(
      'ls-files -tvco --error-unmatch "%s"' % fp)
  if not ok:
    # The file doesn't exist.
    return FILE_NOT_FOUND
  return _status_file(fp)


def au_files(relative_to_cwd=False):
  """Gets all assumed unchanged files.
  
  Args:
    relative_to_cwd: if True then only those au files under the cwd are
      reported. If False, all au files in the repository are reported. (Defaults
      to False.)
  """
  out, unused_err = common.safe_git_call(
      'ls-files -v {}'.format(
          '--full-name "{}"'.format(
              common.repo_dir()) if not relative_to_cwd else ''))
  ret = []
  # There could be dups in the output from ls-files if, for example, there are
  # files in conflict.
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
  return _status_cwd()


# Private functions.


def _status_cwd():
  status_codes = _status_porcelain(os.getcwd())
  au_fps = set(au_files(relative_to_cwd=True))
  for au_fp in au_fps:
    if au_fp not in status_codes:
      status_codes[au_fp] = None
  all_fps_under_cwd = common.get_all_fps_under_cwd()
  for fp_under_cwd in all_fps_under_cwd:
    if fp_under_cwd not in status_codes:
      status_codes[fp_under_cwd] = None
  for s_fp, s in status_codes.iteritems():
    status = _status_from_output(s, s_fp in au_fps, s_fp)
    yield (status, s_fp)


def _status_file(fp):
  s = _status_porcelain(fp).get(fp, None)
  return _status_from_output(s, _is_au_file(fp), fp)


def _is_au_file(fp):
  """True if the given fp corresponds to an assume unchanged file.

  Args:
    fp: the filepath to check (fp must be a file not a dir).
  """
  out, unused_err = common.safe_git_call(
      'ls-files -v --full-name "{}"'.format(fp))
  ret = False
  if out:
    f_out = common.remove_dups(out.splitlines(), lambda x: x[2:])
    if len(f_out) != 1:
      raise Exception('Unexpected output of ls-files: {}'.format(out))
    ret = f_out[0][0] == 'h'
  return ret


def _status_porcelain(pathspec):
  """Executes the status porcelain command with the given pathspec.

  Ignored and untracked files are reported.

  Returns:
    A dict of fp -> status code. All fps are relative to the cwd.
  """
  def sanitize_fp(unsanitized_fp):
    ret = unsanitized_fp.strip()
    if ret.startswith('"') and ret.endswith('"'):
      ret = ret[1:-1]
    # The paths outputted by status are relative to the repodir, we need to make
    # them relative to the cwd.
    ret = os.path.relpath(
        os.path.join(common.repo_dir(), ret), os.getcwd())
    return ret

  out_status, unused_err = common.safe_git_call(
      'status --porcelain -u --ignored "{}"'.format(pathspec))
  ret = {}
  for f_out_status in out_status.splitlines():
    # Output is in the form <status> <file path>.
    # <status> is 2 chars long.
    ret[sanitize_fp(f_out_status[3:])] = f_out_status[:2]
  return ret


def _status_from_output(s, is_au, fp):
  if not s:
    if is_au:
      if not os.path.exists(fp):
        return DELETED_ASSUME_UNCHANGED
      return ASSUME_UNCHANGED
    else:
      return TRACKED_UNMODIFIED
  if s == '??':
    return UNTRACKED
  elif s == '!!':
    return IGNORED
  elif s == ' M':
    return TRACKED_MODIFIED
  elif s == 'A ':
    return STAGED
  elif s == ' D':
    return DELETED
  elif s == 'AD':
    return DELETED_STAGED
  elif s == 'MM':
    return MODIFIED_MODIFIED
  elif s == 'AM':
    return ADDED_MODIFIED
  elif s == 'AA' or s == 'M ' or s == 'DD' or 'U' in s:
    return IN_CONFLICT
  raise Exception('Failed to get status of file {}, s is "{}"'.format(fp, s))
