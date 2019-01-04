# MIX Simulator 

MIX is a hypothetical computer described by Donald Knuth for
instructive use in The Art of Computer Programming. This software
provides a simulator for MIX, written in Python 3, as well as an
assembler for the MIX Assembly Language (MIXAL).

## Development Plan 

The initial scope of this project does not extend to fully emulating a
specific architectural design. That is, accurately specifying a
pipeline and its fetch/execute cycle, enforcing the distinction
between a control unit and an ALU, etc., are not of predominant
concern. However, future releases may broaden the the scope of the
project to accurate representation of such lower-level details.

In the first iteration of the simulated machine, the act of reading or
writing to an external device will be presented as a blocking
operation (that occurs instantaneously). This should have no practical
impact on the execution of correct MIX programs. Later versions of the
machine will allow the user to specify the length of time (or a range
of times) an IO operation will take to complete. Writing and reading
will still occur instantaneously in the background, but this
additional feature will provide a means of exposing incorrect programs
that read or write at inappropriate junctures.
