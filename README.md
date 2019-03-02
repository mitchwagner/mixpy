# MIXpy
MIX is a hypothetical computer described by Donald Knuth for
instructive use in The Art of Computer Programming. MIXpy (pronounced
mix-pea) provides a simulator for MIX, as well as an assembler for the
MIX Assembly Language (MIXAL). MIXpy is written in Python 3, and is
available through PyPI as "mixpy".

## MIX Simulator 
MIXpy realizes the MIX architecture as interactive Python objects.

### Development Plan 

MIX is an instruction set architecture; Knuth does not express a
canonical microarchitecture for its implementation. As such, the scope
of this project is restricted to simulation, rather than emulation,
insofar as the two remain distinguished. That is to say, the
specification of an inspectable pipeline and its fetch/execute cycle,
the maintenance of a separation between a control unit and an ALU,
etc., are not of this project's concern. Such low-level details,
though intellectually interesting, are immaterial to the consideration
of MIX itself.

#### IO 
In the first iteration of the simulated machine, the act of reading or
writing to an external device will be presented as a blocking
operation (that occurs instantaneously). This should have no practical
impact on the execution of correct MIX programs. Later versions of the
machine will allow the user to specify the length of time (or a range
of times) an IO operation will take to complete. Writing and reading
will still occur instantaneously in the background, but this
additional feature will provide a means of exposing incorrect programs
that read or write at inappropriate junctures.

## MIXAL Assembler
MIXAL ("Mix Assembly Language") is a symbolic language designed to
make "MIX programs considerably easier to read and to write, and to
save the programmer from worrying about tediuos clerical details that
often lead to unnecessary errors".

### Syntax
The MIXpy assembler's ultimate goal is to accurately implement the two
formats that Knuth specifies for MIX programs. The first format,
designed for punchards, strictly defines the columns that each MIXAL
instruction field may occupy in a given line. While certainly not
impossible, these constraints complicate the development of a scanner
and parser, requiring either significant lookahead or more ad-hoc
implementations.

Knuth specifies a second format, this for entering MIXAL via a
terminal. Rather than confine the programmer to particular columns
within a line, blank space is used as a delimiter. Unfortunately, this
entails complications for the ALF MIXAL directive operand. In the
Knuth's first format, by virtue of always starting at the 17th
character in a line, the directive is unambiguous- this is no longer
the case in the second format, as the operand can include blank
spaces.

Some implementations of MIXAL parsers work around this by requiring
the use of quotes to delineate the operand to ALF. However, MIXpy will
take a different approach, omitting support for the ALF directive
until proper realization of Knuth's original specification. MIXpy has
no interest in introducing subtle incompatabilities or discrepancies
via the syntax it recognizes. 

## Contribution Guidelines

### Python Version
MIXpy targets Python 3, specifically CPython 3.7.2.

### External Libraries
There is, in general, no compelling reason to introduce dependencies
for MIXpy: those defined in `requirements.txt` concern development and
thus are orthogonal to execution at runtime.

### Conventions 

Following is a series of coding style conventions for contributors to
follow:

#### Strings
Use single quotes for all strings.

#### Method Order
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
