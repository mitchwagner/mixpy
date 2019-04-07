# Assembler

## Assembly Syntax
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
