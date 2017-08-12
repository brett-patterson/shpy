# shpy
Simplified subprocess execution for Python. Currently only supports Python 3.

## Examples

```python
from shpy import echo, grep

result = echo('hello, world\nhi, world') | grep('hello')
# No commands have been executed yet. Accessing the status, stdout, or stderr properties
# on result will trigger the lazy execution.
print(result) # hello, world\n
```
