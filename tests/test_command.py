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
