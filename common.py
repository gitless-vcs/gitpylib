"""Common methods used accross the git-pylib."""


__author__ = "Santiago Perez De Rosso (sperezde@csail.mit.edu)"


import subprocess


def safe_git_call(cmd):
  ok, out, err = git_call(cmd)
  if ok:
    return out, err
  raise Exception('%s failed: out is %s, err is %s' % (cmd, out, err))


def git_call(cmd):
  p = subprocess.Popen(
      'git %s' % cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
      shell=True)
  out, err = p.communicate()
  return p.returncode == 0, out, err
