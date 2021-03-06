import subprocess
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class ShpyStatusException(Exception):
    def __init__(self, command, status, stdout, stderr):
        super(ShpyStatusException, self).__init__(
            'Status %d returned from command \'%s\'' % (status, ' '.join(command))
        )

        self.command = command
        self.status = status
        self.stdout = stdout
        self.stderr = stderr


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

    def __gt__(self, dest):
        return ShpyCommandRedirect(self, dest)


class ShpyCommand(ShpyCommandBase):
    """ A command that executes a single subprocess command.
    """
    def __init__(self, command, throw=True):
        super(ShpyCommand, self).__init__()
        self._command = command
        self._throw = throw

    def execute(self, stdin=None):
        proc = subprocess.Popen(self._command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(stdin)

        status = proc.returncode
        stdout = stdout.strip()
        stderr = stderr.strip()

        if status != 0 and self._throw:
            raise ShpyStatusException(self._command, status, stdout, stderr)

        return status, stdout.strip(), stderr.strip()


class ShpyCommandPipe(ShpyCommandBase):
    """ A command that pipes the output of one command to the input of another.
    """
    def __init__(self, left, right):
        super(ShpyCommandPipe, self).__init__()
        self.left = left
        self.right = right

    def execute(self, stdin=None):
        _, stdout, _ = self.left.execute(stdin)
        return self.right.execute(stdout)


class ShpyCommandRedirect(ShpyCommandBase):
    """ A command that redirects the output of one command to a file.
    """
    def __init__(self, command, dest):
        super(ShpyCommandRedirect, self).__init__()
        self.command = command
        self.dest = dest

        # Evaluate the command immediately
        self.execute()

    def execute(self, stdin=None):
        _, stdout, _ = self.command.execute(stdin)
        if hasattr(self.dest, 'write'):
            # File-like object
            self.dest.write(stdout)
        elif isinstance(self.dest, str) or isinstance(self.dest, bytes):
            with open(self.dest, 'wb') as dest_file:
                dest_file.write(stdout)
        else:
            raise TypeError('Invalid redirection destination: {}'.format(self.dest))

        return 0, b'', b''
