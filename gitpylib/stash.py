# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for dealing with Git stashes."""


import common

import re


def all(msg):
  """Creates a stash with the given msg that contains all local changes.

  This will add to the stash both the untracked and ignored files.

  Args:
    msg: the msg for the stash to create.
  """
  common.safe_git_call('stash save --all -- "%s"' % msg)


def pop(msg):
  """Pop the stash that has the given msg (if found).

  Args:
    msg: the message corresponding to the stash to pop.
  """
  s_id = _stash_id(msg)
  if not s_id:
    return

  common.safe_git_call('stash pop %s' % s_id)


def drop(msg):
  """Drop the stash that has the given msg (if found).

  Args:
    msg: the message corresponding to the stash to drop.
  """
  s_id = _stash_id(msg)
  if not s_id:
    return

  common.safe_git_call('stash drop %s' % s_id)


def _stash_id(msg):
  """Gets the stash id of the stash with the given msg.

  Args:
    msg: the message of the stash to retrieve.

  Returns:
    the stash id of the stash with the given msg or None if no matching stash is
    found.
  """
  out, unused_err = common.safe_git_call('stash list --grep=": %s"' % msg)

  if not out:
    return None

  pattern = '(stash@\{.+\}): '
  result = re.match(pattern, out)
  if not result:
    raise Exception('Unexpected output %s' % out)

  return result.group(1)
