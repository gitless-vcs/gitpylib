"""Sync module for Git sync operations."""


import os

import common


SUCCESS = 1
LOCAL_CHANGES_WOULD_BE_LOST = 2
NOTHING_TO_MERGE = 3
CONFLICT = 4


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


def commit_include(files, msg):
  """Record changes in the local repository.

  Before making a commit of changes staged so far, the files given are staged.
  
  Args:
    files: the files to stage before commiting.
    msg: the commit message.

  Returns:
    The output of the commit command.
  """
  out, unused_err = common.safe_git_call('commit -m\"%s\" -i %s' % (msg, ' '.join(files)))
  return out


# TODO(sperezde): it seems like src could also be a commit point.
def merge(src):
  """Merges changes in the src branch into the current branch.

  Args:
    src: the source branch to pick up changes from.

  Returns:
    - LOCAL_CHANGES_WOULD_BE_LOST
  """
  ok, out, err = common.git_call('merge %s' % src)
  print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    if out.startswith('Auto-merging'):
      # conflict?
      raise Exception('conflict?')
    else:
      return (LOCAL_CHANGES_WOULD_BE_LOST, err.splitlines()[1:-2])
  if out == 'Already up-to-date.\n':
    return (NOTHING_TO_MERGE, None)
  return (SUCCESS, None)


def abort_merge():
  """Aborts the current merge."""
  common.safe_git_call('merge --abort')


def merge_in_progress():
  return os.path.exists(os.path.join(common.git_dir(), 'MERGE_HEAD'))


def rebase(new_base):
  ok, out, err = common.git_call('rebase %s' % new_base)
  print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    return (CONFLICT, ['tbd1', 'tbd2'])
  return (SUCCESS, out)


def abort_rebase():
  common.safe_git_call('rebase --abort')


def rebase_in_progress():
  return os.path.exists(os.path.join(common.git_dir(), 'rebase-apply'))
