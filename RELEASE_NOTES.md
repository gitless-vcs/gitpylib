Gitpylib's Release Notes
========================


25th Mar 2014 - 0.6
-------------------

* Unset upstream support.
* Better wrapping of `git log`.
* Apply patch suppport.
* Return # of additions and deletions in diff.
* Bug fixes and code cleanups.


3rd Feb 2014 - 0.5
------------------

* gitpylib now works in python 2.6, 3.2 and 3.3 (in addition to 2.7).
* Added a function to get the names of the branches in a remote.
* remote.add will also do a fetch.
* Bug fixes and code cleanups.


16th Jan 2014 - 0.4.3
---------------------

* More performance improvements in status.
* Added an option to not report tracked unmodified files if desired (which makes
  status much faster if the caller doesn't care about knowing which files are
  tracked unmodified).


15th Jan 2014 - 0.4.2
---------------------

* Performance improvements in status.
* Output of log is piped to less.


6th Dec 2013 - 0.4.1
--------------------

* Bug fixes (in diff and PyPI setup).


23rd Nov 2013 - 0.4
-------------------

* Machine-friendly output of diff command.


(No notes for previous releases)
