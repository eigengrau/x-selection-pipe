from threading import Lock

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Selection:
    """Monitor a selection and perform an action when its owner changes."""

    def __init__(self, selection, actions=[]):

        self.selection = Gtk.Clipboard.get(selection)
        self.actions = []
        self.lock = Lock()
        for action in actions:
            self.add_action(action)

    def add_action(self, func):

        self.actions.append(func)

    def connect(self):

        self.selection.connect('owner-change', self.on_change)

    def on_change(self, *args):

        # Avoid recursing on change events infinitely in cases where we trigger
        # an owner changes ourselves.
        if self.acquire(blocking=False):

            text = self.selection.wait_for_text()
            if text:
                for action in self.actions:
                    action(text)
            self.release()

        else:
            # Since we’ve just inhibited the recursive event, we can lift the
            # inhibition.
            self.release()

    def set(self, text):

        self.acquire()
        self.selection.set_text(text, -1)

    def acquire(self, *args, **kwargs):

        result = self.lock.acquire(*args, **kwargs)
        return result

    def release(self, *args, **kwargs):

        result = self.lock.release(*args, **kwargs)
        return result
