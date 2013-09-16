# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.


import subprocess


def log():
  subprocess.call('git log', shell=True)


def log_p():
  subprocess.call('git log -p', shell=True)
