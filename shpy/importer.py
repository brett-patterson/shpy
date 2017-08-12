import imp
import re
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec

from .command import ShpyCommandWrapper


PACKAGE_NAME_PATTERN = r'^shpy\.([^\.]+)$'


class ShpyPathFinder(MetaPathFinder):
    """ A custom path finder for Python's import mechanism that supports
    importing missing names from the shpy namespace as shell commands.
    """
    def find_spec(self, fullname, path, target=None):
        match = re.match(PACKAGE_NAME_PATTERN, fullname)
        if match is None:
            return None
        return ModuleSpec(fullname, ShpyLoader(match.group(1)))


class ShpyLoader(Loader):
    def __init__(self, command):
        super().__init__()
        self._command = command

    def create_module(self, spec):
        return ShpyCommandWrapper(self._command)

    def exec_module(self, mod):
        pass
