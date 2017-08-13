import tempfile
from StringIO import StringIO

from .base_test import BaseTest

class TestCommand(BaseTest):
    """ Tests the various command operations.
    """
    def test_command_basic(self):
        from shpy import echo

        result = echo('foo', 'bar')
        self.assertEqual(0, result.status)
        self.assertEqual('foo bar', result.stdout)
        self.assertEqual('', result.stderr)

    def test_command_basic_fail(self):
        from shpy import test, ShpyStatusException

        try:
            str(test())
        except ShpyStatusException as exc:
            self.assertEqual(1, exc.status)
            self.assertEqual('', exc.stdout)
            self.assertEqual('', exc.stderr)
        else:
            self.fail('Status exception not thrown')

    def test_command_pipe(self):
        from shpy import echo, grep

        result = echo('hello, world\nhi, world') | grep('hello')
        self.assertEqual(0, result.status)
        self.assertEqual('hello, world', result.stdout)
        self.assertEqual('', result.stderr)

    def test_command_pipe_fail(self):
        from shpy import echo

        try:
            echo('test') | []
        except TypeError:
            pass
        else:
            self.fail('Type error not thrown')

    def test_command_pipe_fail_early(self):
        from shpy import test, grep, ShpyStatusException

        try:
            str(test() | grep('hello'))
        except ShpyStatusException as exc:
            self.assertEqual(1, exc.status)
            self.assertEqual('', exc.stdout)
            self.assertEqual('', exc.stderr)
        else:
            self.fail('Status exception not thrown')

    def test_command_redirect(self):
        from shpy import echo

        s = StringIO()
        echo('testing') > s
        s.seek(0)
        self.assertEqual('testing', s.read())

        with tempfile.NamedTemporaryFile() as tmp_file:
            echo('testing') > tmp_file.name
            tmp_file.seek(0)
            self.assertEqual('testing', tmp_file.read())

    def test_command_redirect_fail(self):
        from shpy import echo

        try:
            echo('foo') > 0
        except TypeError:
            pass
        else:
            self.fail('Type error not thrown')
