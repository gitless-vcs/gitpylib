"""Sync module for Git sync operations."""


import common


def commit(files, msg):
  """Record changes in the local repository.
  
  Args:
    files: the files to commit.
    msg: the commit message.

  Returns:
    The output of the commit command.
  """
  out, unused_err = common.safe_git_call('commit -m\"%s\" %s' % (msg, ' '.join(files)))
  return out
