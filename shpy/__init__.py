import sys
from .module import ShpyModule

mod = sys.modules[__name__]
sys.modules[__name__] = ShpyModule(mod)
