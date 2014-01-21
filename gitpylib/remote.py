# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for dealing with Git remotes."""


import common


SUCCESS = 1
REMOTE_NOT_FOUND = 2
REMOTE_UNREACHABLE = 3
REMOTE_BRANCH_NOT_FOUND = 4


def add(remote_name, remote_url):
  """Adds the given remote.

  Args:
    remote_name: the name of the remote to add.
    remote_url: the url of the remote to add.

  Returns:
    SUCCESS or REMOTE_UNREACHABLE.
  """
  if _show(remote_url)[0] == REMOTE_UNREACHABLE:
    return REMOTE_UNREACHABLE
  common.safe_git_call('remote add %s %s' % (remote_name, remote_url))
  return SUCCESS


def show(remote_name):
  """Get information about the given remote.

  Args:
    remote_name: the name of the remote to get info from.

  Returns:
    a tuple (status, out) where status is one of SUCCESS, REMOTE_NOT_FOUND, or
    REMOTE_UNREACHABLE and out is the output of the show command on success.
  """
  if remote_name not in show_all():
    return (REMOTE_NOT_FOUND, None)
  return _show(remote_name)


def show_all():
  """Get information of all the remotes."""
  out, unused_err = common.safe_git_call('remote')
  return out.splitlines()


def rm(remote_name):
  common.safe_git_call('remote rm %s' % remote_name)


def head_exist(remote_name, head):
  ok, out, unused_err = common.git_call(
      'ls-remote --heads %s %s' % (remote_name, head))
  if not ok:
    return (False, REMOTE_UNREACHABLE)
  return (len(out) > 0, REMOTE_BRANCH_NOT_FOUND)


def branches(remote_name):
  """Gets the name of the branches in the given remote."""
  out, err = common.safe_git_call('branch -r')
  remote_name_len = len(remote_name)
  for line in out.splitlines():
    if '->' in line:
      continue
    line = line.strip()
    if line.startswith(remote_name):
      yield line[remote_name_len+1:]


# Private functions.


def _show(remote):
  ok, out, err = common.git_call('remote show %s' % remote)
  if not ok:
    if 'fatal: Could not read from remote repository' in err:
      return (REMOTE_UNREACHABLE, None)
    else:
      raise Exception('Unexpected output %s, err %s' % (out, err))
  return (SUCCESS, out)
