# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.


import subprocess


def log():
  # The pipe to less shouldn't be here. TODO: fix.
  subprocess.call('git log | less', shell=True)


def log_p():
  # The pipe to less shouldn't be here. TODO: fix.
  subprocess.call('git log -p | less', shell=True)
