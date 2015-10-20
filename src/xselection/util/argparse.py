"""The default Python argument parser doesn’t allow supplying list-valued
defaults to options for which a set of 'choices' are defined. This extends the
default ArgumentParser by the action 'list_choices', which allows for
list-valued defaults.

"""


import argparse


__all__ = ('ArgumentParser')


class ArgumentParser (argparse.ArgumentParser):
    """An argument parser which extends the default ArgumentParser by an action
    'list_choices', which allows specifying a set of 'choices', but allows for a
    list-valued default.

    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs,
                         formatter_class=DefaultListActionFormatter)
        self.register('action', 'list_choices', DefaultListAction)


class DefaultListActionFormatter (argparse.ArgumentDefaultsHelpFormatter):

    def _metavar_formatter(self, action, default_metavar):

        if isinstance(action, DefaultListAction):

            choice_strs = [str(choice) for choice in action.list_choices]
            result = '{%s}' % ','.join(choice_strs)

            def format(tuple_size):

                if isinstance(result, tuple):
                    return result
                else:
                    return (result, ) * tuple_size

            return format

        else:
            return super()._metavar_formatter(action, default_metavar)


class DefaultListAction (argparse.Action):

    def __init__(self, *args, **kwargs):

        try:
            self.list_choices = kwargs['list_choices']
            del kwargs['list_choices']
        except KeyError:
            raise TypeError("Missing keyword-argument: 'list_choices'.")

        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string='fohiea'):

        for value in values:
            if value not in self.list_choices:
                msg = "Invalid selection: %s" % value
                raise argparse.ArgumentError(self, msg)
        else:
            setattr(namespace, self.dest, values)
