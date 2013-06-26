"""Sync module for Git sync operations."""


import os
import re

import common


SUCCESS = 1
LOCAL_CHANGES_WOULD_BE_LOST = 2
NOTHING_TO_MERGE = 3
NOTHING_TO_REBASE= 4
CONFLICT = 5
NOTHING_TO_PUSH = 6


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
    #if out.startswith('Auto-merging'):
      # conflict?
    #  raise Exception('conflict?')
    if 'Automatic merge failed; fix conflicts and then commit the result.' in out:
      return (CONFLICT, None)
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
    if err == (
        'Cannot rebase: You have unstaged changes.\nPlease commit or stash '
        'them.\n'):
      # TODO(sperezde): add the files whose changes would be lost.
      return (LOCAL_CHANGES_WOULD_BE_LOST, None)
    return (CONFLICT, None)
  if re.match('Current branch \w+ is up to date.\n', out):
    return (NOTHING_TO_REBASE, None)
  return (SUCCESS, out)


def rebase_continue():
  ok, out, err = common.git_call('rebase --continue')
  print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    return (CONFLICT, None)
  return (SUCCESS, out)

def skip_rebase_commit():
  ok, out, err = common.git_call('rebase --skip')
  print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    return (CONFLICT, ['tbd1', 'tbd2'])
  return (SUCCESS, out)


def abort_rebase():
  common.safe_git_call('rebase --abort')


def rebase_in_progress():
  return os.path.exists(os.path.join(common.git_dir(), 'rebase-apply'))


def push(src_branch, dst_remote, dst_branch):
  out, err = common.safe_git_call('push %s %s:%s' % (dst_remote, src_branch, dst_branch))
  if err == 'Everything up-to-date\n':
    return (NOTHING_TO_PUSH, None)
  # Not sure why, but git push returns output in stderr.
  return (SUCCESS, err)
