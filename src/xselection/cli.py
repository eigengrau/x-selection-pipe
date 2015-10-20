"""Monitor Xorg selections, optionally sync them, and print changes to
stdout.

"""

import signal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from xselection.selection import Selection
from xselection.util.argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument(
    '--sync', '-s',
    dest='sync_selections',
    default=False,
    action='store_true',
    help='Sync primary selection and clipboard on changes.'
)

parser.add_argument(
    'targets',
    nargs='*',
    action='list_choices',
    list_choices=('primary', 'clipboard'),
    default=('primary', 'clipboard'),
    help="The set of selections to monitor."
)


def print_for_selection(text):

    print(text, flush=True)


def main():

    args = parser.parse_args()

    monitor_clipboard = 'clipboard' in args.targets
    monitor_primary = 'primary' in args.targets

    if monitor_primary:
        primary = Selection(Gdk.SELECTION_PRIMARY)
        primary.add_action(print_for_selection)

    if monitor_clipboard:
        clipboard = Selection(Gdk.SELECTION_CLIPBOARD)
        clipboard.add_action(print_for_selection)

    monitor_both = monitor_primary and monitor_clipboard
    if monitor_both and args.sync_selections:
        primary.add_action(clipboard.set)
        clipboard.add_action(primary.set)

    if monitor_primary:
        primary.connect()
    if monitor_clipboard:
        clipboard.connect()

    # Work around bug 622084.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
