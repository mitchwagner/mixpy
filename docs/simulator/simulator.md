# MIXpy Simulator

## Scope 

MIX is an instruction set architecture; Knuth does not provide a
canonical microarchitecture for its implementation. As such, the scope
of this project is restricted to simulation, rather than emulation,
insofar as the two remain distinguished. That is to say, the
specification of an inspectable pipeline and its fetch/execute cycle,
the maintenance of a separation between a control unit and an ALU,
etc., are not of this project's concern. Such low-level details,
though intellectually interesting, are immaterial to the consideration
of MIX itself.

## IO
In the first iteration of the simulated machine, the act of reading or
writing to an external device will be presented as a blocking
operation (that occurs instantaneously). This should have no practical
impact on the execution of correct MIX programs. Later versions of the
machine will allow the user to specify the length of time (or a range
of times) an IO operation will take to complete. Writing and reading
will still occur instantaneously in the background, but this
additional feature will provide a means of exposing incorrect programs
that read or write at inappropriate junctures.
