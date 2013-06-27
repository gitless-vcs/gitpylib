import common


def clone(repo):
  common.safe_git_call('clone %s .' % repo)


def init():
  common.safe_git_call('init')
