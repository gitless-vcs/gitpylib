"""Module for dealing with Git files."""


__author__ = "Santiago Perez De Rosso (sperezde@csail.mit.edu)"


SUCCESS = 1
FILE_NOT_FOUND = 2


def stage(fp):
  """Stages the given file.
  
  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed sucessfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  # TBD


def assume_unchanged(fp):
  """Marks the given file as assumed-unchanged.

  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed sucessfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  # TBD


def not_assume_unchanged(fp):
  """Unmarks the given assumed-unchanged file.

  Args:
    fp: the path of the file to stage (e.g., 'paper.tex').

  Returns:
    - SUCCESS: the operation completed sucessfully.
    - FILE_NOT_FOUND: the given file doesn't exist.
  """
  # TBD
