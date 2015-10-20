from collections import deque

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Selection:
    """Monitor a selection and perform an action when its owner changes."""

    def __init__(self, selection, actions=[]):

        self.selection = Gtk.Clipboard.get(selection)
        self.actions = []
        self.ignore_once = deque()
        for action in actions:
            self.add_action(action)

    def add_action(self, func):

        self.actions.append(func)

    def connect(self):

        self.selection.connect('owner-change', self.on_change)

    def on_change(self, *args):

        text = self.selection.wait_for_text()

        if not text:
            return

        # Avoid recursing on change events infinitely in cases where we trigger
        # an owner change ourselves.
        if self.ignore_once and self.ignore_once[0] == text:
            self.ignore_once.popleft()
            return

        for action in self.actions:
            action(text)

    def set(self, text):

        self.ignore_once.append(text)
        self.selection.set_text(text, -1)
