from types import ModuleType

from .command import ShpyCommandWrapper


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
