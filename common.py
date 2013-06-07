"""Common methods used accross the git-pylib."""


__author__ = "Santiago Perez De Rosso (sperezde@csail.mit.edu)"


import os
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


def fix_case(fp):
  """Returns the same filepath with the correct casing.
 
  In UNIX filenames are case-insensitive, meaning that "README" is the same
  thing as "readme" or "ReaDmE" but in Windows these would be different.
  Git commands are case-sensitive but the gitpylib is case-insensitive if
  executing in UNIX and case-sensitive in Windows thus making its behaviour
  consistent with the OS. This method is used to normalize the filepath before
  passing it to a Git command.

  Args:
    fp: the filepath to case-correct. It should correspond to an existing file.

  Returns:
    The same filepath with the correct casing (OS-dependent).
  """
  # TODO(sperezde): if windows => do nothing
  bn = os.path.basename(fp)
  for f in os.listdir(os.path.dirname(os.path.abspath(fp))):
    if f.lower() == bn.lower():
      return f
  raise Exception("Invalid file %s: the file doesn't exist" % fp)
