import sys
from .importer import ShpyPathFinder

sys.meta_path.append(ShpyPathFinder())
