from .base_test import BaseTest

class TestModule(BaseTest):
    """ Tests importing from the module shim.
    """
    def test_import_exists(self):
        from shpy.command import ShpyCommandBase

    def test_import_command(self):
        from shpy.module import ShpyCommandWrapper
        from shpy import ls
        self.assertIsInstance(ls, ShpyCommandWrapper)
