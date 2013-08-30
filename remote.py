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
  """Adds the given remote."""
  common.safe_git_call('remote add %s %s' % (remote_name, remote_url))


def list():
  """Returns a list with all the remotes."""
  out, unused_err = common.safe_git_call('remote')
  return out.splitlines()


def show(remote_name):
  """Get information about the given remote.

  Args:
    remote_name: the name of the remote to get info from.

  Returns:
    None if remote doesn't exist or the output of the cmd if otherwise.
  """
  ok, out, err = common.git_call('remote show %s' % remote_name)
  if not ok:
    if 'fatal: Could not read from remote repository' in err:
      return (REMOTE_UNREACHABLE, None)
    else:
      raise Exception('Unexpected output %s, err %s' % (out, err))
  if not out:
    return (REMOTE_NOT_FOUND, None)
  return (SUCCESS, out)


def rm(remote_name):
  common.safe_git_call('remote rm %s' % remote_name)


def head_exist(remote_name, head):
  ok, out, unused_err = common.git_call(
      'ls-remote --heads %s %s' % (remote_name, head))
  if not ok:
    return (False, REMOTE_UNREACHABLE)
  return (len(out) > 0, REMOTE_BRANCH_NOT_FOUND)
