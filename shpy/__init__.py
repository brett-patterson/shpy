import sys
from .module import ShpyModule
from .command import ShpyStatusException

mod = sys.modules[__name__]
sys.modules[__name__] = ShpyModule(mod)
