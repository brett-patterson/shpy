import subprocess
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class ShpyCommandWrapper:
    """ A callable wrapper for a command.
    """
    def __init__(self, name):
        self._name = name

    def __call__(self, *args):
        return ShpyCommand([self._name] + list(args))


class ShpyCommandBase(with_metaclass(ABCMeta)):
    """ The base class for a command. Subclasses must implement the execute
    method.
    """
    def __init__(self):
        self._executed = False
        self._status = None
        self._stdout = None
        self._stderr = None

    @property
    def status(self):
        self._execute()
        return self._status

    @property
    def stdout(self):
        self._execute()
        return self._stdout

    @property
    def stderr(self):
        self._execute()
        return self._stderr

    @abstractmethod
    def execute(self, stdin=None):
        return None, None, None

    def _execute(self):
        if not self._executed:
            self._status, self._stdout, self._stderr = self.execute()
            self._executed = True

    def __bytes__(self):
        return self.stdout

    def __str__(self):
        return self.stdout.decode()

    def __repr__(self):
        return str(self).strip()

    def __or__(self, other):
        if not isinstance(other, ShpyCommandBase):
            raise TypeError('Object {} must be a subclass of ShpyCommandBase'.format(other))

        return ShpyCommandPipe(self, other)


class ShpyCommand(ShpyCommandBase):
    """ A command that executes a single subprocess command.
    """
    def __init__(self, command):
        super(ShpyCommand, self).__init__()
        self._command = command

    def execute(self, stdin=None):
        proc = subprocess.Popen(self._command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(stdin)
        status = proc.returncode
        return status, stdout, stderr


class ShpyCommandPipe(ShpyCommandBase):
    """ A command that pipes the output of one command to the input of another.
    """
    def __init__(self, left, right):
        super(ShpyCommandPipe, self).__init__()
        self.left = left
        self.right = right

    def execute(self, stdin=None):
        status, stdout, stderr = self.left.execute(stdin)
        if status != 0:
            return status, stdout, stderr

        return self.right.execute(stdout)
