# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Sync module for Git sync operations."""


import os
import re

import common


SUCCESS = 1
LOCAL_CHANGES_WOULD_BE_LOST = 2
NOTHING_TO_MERGE = 3
NOTHING_TO_REBASE = 4
CONFLICT = 5
NOTHING_TO_PUSH = 6
PUSH_FAIL = 7


def commit(files, msg, skip_checks=False, stage_files=False):
  """Record changes in the local repository.

  Args:
    files: the files to commit.
    msg: the commit message.
    skip_checks: if the pre-commit hook should be skipped or not (defaults to
      False).
    stage_files: whether to stage the given files before commiting or not.

  Returns:
    the output of the commit command.
  """
  out, unused_err = common.safe_git_call(
      'commit {}{}-m"{}" "{}"'.format(
          '--no-verify ' if skip_checks else '',
          '-i ' if stage_files else '',
          msg, '" "'.join(files)))
  return out


def merge(src):
  """Merges changes in the src branch into the current branch.

  Args:
    src: the source branch to pick up changes from.
  """
  ok, out, err = common.git_call('merge %s' % src)
  return _parse_merge_output(ok, out, err)


def _parse_merge_output(ok, out, err):
  # print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    #if out.startswith('Auto-merging'):
      # conflict?
    #  raise Exception('conflict?')
    if ('Automatic merge failed; fix conflicts and then commit the result.'
            in out):
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
  return _parse_rebase_output(ok, out, err)


def _parse_rebase_output(ok, out, err):
  # print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    if err == (
        'Cannot rebase: You have unstaged changes.\nPlease commit or stash '
        'them.\n'):
      # TODO(sperezde): add the files whose changes would be lost.
      return (LOCAL_CHANGES_WOULD_BE_LOST, None)
    elif ('The following untracked working tree files would be overwritten'
          in err):
      # TODO(sperezde): add the files whose changes would be lost.
      return (LOCAL_CHANGES_WOULD_BE_LOST, None)
    return (CONFLICT, None)
  if re.match('Current branch [^\s]+ is up to date.\n', out):
    return (NOTHING_TO_REBASE, None)
  return (SUCCESS, out)


def rebase_continue():
  ok, out, err = common.git_call('rebase --continue')
  # print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    return (CONFLICT, None)
  return (SUCCESS, out)


def skip_rebase_commit():
  ok, out, err = common.git_call('rebase --skip')
  # print 'out is <%s>, err is <%s>' % (out, err)
  if not ok:
    return (CONFLICT, ['tbd1', 'tbd2'])
  return (SUCCESS, out)


def abort_rebase():
  common.safe_git_call('rebase --abort')


def rebase_in_progress():
  return os.path.exists(os.path.join(common.git_dir(), 'rebase-apply'))


def push(src_branch, dst_remote, dst_branch):
  ok, out, err = common.git_call(
      'push %s %s:%s' % (dst_remote, src_branch, dst_branch))
  if err == 'Everything up-to-date\n':
    return (NOTHING_TO_PUSH, None)
  elif ('Updates were rejected because a pushed branch tip is behind its remote'
        in err):
    return (PUSH_FAIL, None)
  # Not sure why, but git push returns output in stderr.
  return (SUCCESS, err)


def pull_rebase(remote, remote_b):
  ok, out, err = common.git_call('pull --rebase %s %s' % (remote, remote_b))
  return _parse_rebase_output(ok, out, err)


def pull_merge(remote, remote_b):
  ok, out, err = common.git_call('pull %s %s' % (remote, remote_b))
  return _parse_merge_output(ok, out, err)
