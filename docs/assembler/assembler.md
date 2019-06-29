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

## Parser Implementation
As defined, Knuth's MIXAL is not readily amenable to an elegant recursive
descent parser, thanks to the significance of character line columns and the
ambiguity in each line, where most fields are optional. For example, each MIXAL
line can begin with an optional label, and there's no reason that label cannot
be a string that also corresponds to an opcode. Thus, determining whether or
not to treat such a token as a label or an opcode requires looking through the
next few tokens, precluding an LL(1) parser.

Nevertheless, one _can_ create an LL(1) parser for MIXAL, providing the right
token set is used. This can be achieved by shunting some of the semantic
interpretation off to the scanner, transforming it from a "pure" regular
language recognizer to one that maintains state to distinguish different fields
from one another. This is, of course, not the only choice- we could leak
lexical information to the parser, or perhaps design an LL(k) parser- but it
mantains simplicity of implementation and a strong separation between the two
concerns.

### Grammar

To implement the parser, we utilize the following grammar, denoted in EBNF
(whitespace in the following productions should be ignored):

- program -> line {line}

- line -> label instr 

- instr -> op fields 
- instr -> pseudo-1 w-val
- instr -> pseudo-2 str

- fields -> {a-part},{index-part}{f-part}

- a-part -> eps | expr | literal | future-ref

- index-part -> eps | expr

- f-part -> eps | (expr)

- expr -> [+ | -] atom expr'
- expr' -> binary-op atom expr' | eps

- atom -> num | defined-symbol | *

- binary-op -> + | - | * | / | // | :

- literal -> = w-val =

- w-val -> expr f-part
- w-val -> expr f-part , w-val

Notes: 
- "eps" is the epsilon production
