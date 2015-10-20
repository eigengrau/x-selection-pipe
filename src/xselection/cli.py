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
    list_choices=('primary', 'secondary', 'clipboard'),
    default=('primary', 'secondary', 'clipboard'),
    help="The set of selections to monitor."
)


def print_for_selection(text):

    print(text, flush=True)


def main():

    args = parser.parse_args()

    selection_atom = {
        'primary': Gdk.SELECTION_PRIMARY,
        'secondary': Gdk.SELECTION_SECONDARY,
        'clipboard': Gdk.SELECTION_CLIPBOARD
    }

    selections = []
    for target in args.targets:

        atom = selection_atom[target]
        selection = Selection(atom)
        selection.add_action(print_for_selection)
        selections.append(selection)

    if args.sync_selections:

        # Synchronization is achieved by connecting all selections in a cirular
        # graph.
        pairwise = zip(selections[:-1], selections[1:])
        for (selection1, selection2) in pairwise:
            selection1.add_action(selection2.set)
            selection2.add_action(selection1.set)

        # Tie up the circle.
        first, last = selections[0], selections[-1]
        last.add_action(first.set)
        first.add_action(last.set)

    for selection in selections:
        selection.connect()

    # Work around bug 622084.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
