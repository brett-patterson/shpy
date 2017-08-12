import subprocess
from abc import ABCMeta, abstractmethod


class ShpyCommandWrapper:
    def __init__(self, name):
        self._name = name

    def __call__(self, *args):
        return ShpyCommand([self._name] + list(args))


class ShpyCommandBase(metaclass=ABCMeta):
    def __init__(self):
        self._executed = False

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

    def __bytes__(self):
        return self.stdout

    def __str__(self):
        return self.stdout.decode()

    def __repr__(self):
        return str(self).strip()

    def __or__(self, other):
        if not isinstance(other, ShpyCommandBase):
            raise TypeError(f'Object {other} must be a subclass of ShpyCommandBase')

        return ShpyCommandPipe(self, other)


class ShpyCommand(ShpyCommandBase):
    def __init__(self, command):
        super().__init__()
        self._command = command

    def execute(self, stdin=None):
        proc = subprocess.Popen(self._command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(stdin)
        status = proc.returncode
        return status, stdout, stderr


class ShpyCommandPipe(ShpyCommandBase):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def execute(self, stdin=None):
        status, stdout, stderr = self.left.execute(stdin)
        if status != 0:
            return status, stdout, stderr

        return self.right.execute(stdout)
