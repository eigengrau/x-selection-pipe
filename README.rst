x-selection-pipe
================

x-selection-pipe monitors the Xorg clipboard resp. primary selection, piping all
changes to stdout. Optionally, clipboard and primary selection will be kept in
sync.


Rationale
---------

While there is no apparent lack of clipboard monitoring daemons, none of those I
had tried allowed for programmable shell actions to be triggered by clipboard
changes. One of the obstacles I had encountered is that the program interface
would allow for isolated queries to clipboard history, but would not provide for
an on-going text-based stream of clipboard changes (except by resorting to
polling). x-selection-pipe is meant to provide just this sort of streaming
interface, which can then be used to feed clipboard events into shell pipelines.


Usage
-----

::

  usage: xselection-pipe [-h] [--sync]
                         [{primary,clipboard} [{primary,clipboard} ...]]

  positional arguments:
    {primary,clipboard}  The set of selections to monitor. (default: ('primary',
                         'clipboard'))

  optional arguments:
    -h, --help           show this help message and exit
    --sync, -s           Sync primary selection and clipboard on changes.
                         (default: False)


Requirements
------------

x-selection-pipe relies on Gtk+ 3 and pygobject.


TODO
----

- Implement a complementing (but separate) program which supports a
  kill-ring-like clipboard stack
