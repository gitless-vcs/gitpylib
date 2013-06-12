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
    msg: the msg under it which was stashed.
  """
  out, unused_err = common.safe_git_call('stash list --grep=": %s"' % msg)

  if not out:
    return

  pattern = '(stash@\{.+\}): '
  result = re.match(pattern, out)
  if not result:
    raise Exception('Unexpected output %s' % out)

  common.safe_git_call('stash pop %s' % result.group(1))
