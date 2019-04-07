# Contribution Guidelines 

## Python Version
MIXpy targets Python 3, specifically CPython 3.7.2.

## External Libraries
There is, in general, no compelling reason to introduce dependencies
for MIXpy: those defined in `requirements.txt` concern development and
thus are orthogonal to execution at runtime.

## Conventions 

Following is a series of coding style conventions for contributors to
follow:

### Strings
Use single quotes for all strings.

### Method Order
Functions should be implemented, as much as possible, in "call-stack
order", e.g.:

```python
def foo():
    ...
    bar()
    ...
    baz()
    ...

def bar():
    ...
    a()
    ...

def a():
    ...

def baz()
    ...
```
