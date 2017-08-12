from types import ModuleType

from .command import ShpyCommand


class ShpyCommandWrapper:
    """ A callable wrapper for a command.
    """
    def __init__(self, name):
        self._name = name

    def __call__(self, *args):
        return ShpyCommand([self._name] + list(args))


class ShpyModule(ModuleType):
    """ A module shim that treats unrecognized attributes as command names.
    """
    def __init__(self, mod):
        self._mod = mod

    def __getattr__(self, key):
        val = getattr(self._mod, key, None)
        if val is not None:
            return val

        return ShpyCommandWrapper(key)
