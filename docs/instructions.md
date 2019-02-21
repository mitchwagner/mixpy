# Instruction Format
In MIX, each instruction has six fields, taking the form

| 0  | 1 | 2 | 3 | 4 | 5 |
| -- | - | - | - | - | - |
| +- | A | A | I | F | C |

The fields have the following significance:

- C: the operation code, specifying the operation to be performed

- F: an operation code modifier, usually a field specification of the
  form (L:R) = (8L + R).

- +-AA: a memory address.

- I: index specification, used to modify the effective address. If
  I=0, the address +-AA is used without modification. Otherwise, I
  should contain a number i between 1 and 6 (inclusive), and the contents
  of register Ii are added, algebraically to +-AA before the
  instruction is carried out. 

Knuth utilizes the following additional shorthands:

- M: the address, after indexing has occured
- V: the field-specified value M

# Instructions

Following is a list of the 64 instructions that Knuth provides for in his
specification.

| Name | Op Code | Description  |
| ---- | ------- | ------------ |
| NOP  | 0       | No operation |
| ADD  | 1       |              |
| SUB  | 2       |              |
| MUL  | 3       |              |
| DIV  | 4       |              |
| Special     | 5       |              |
| SLA, SRA, SLAX, SRAX, SLC, SRC | 6       |              |
| MOVE     | 7       |              |
| LDA     | 8       |              |
| LD1     | 9      |              |
| LD2     | 10      |              |
| LD3     | 11      |              |
| LD4     | 12      |              |
| LD5     | 13      |              |
| LD6     | 14      |              |
| LDX     | 15      |              |
| LDAN     | 16      |              |
| LD1N     | 17      |              |
| LD2N     | 18      |              |
| LD3N     | 19      |              |
| LD4N     | 20      |              |
| LD5N     | 21      |              |
| LD6N     | 22      |              |
| LDXN     | 23      |              |
| STA     | 24      |              |
| ST1     | 25      |              |
| ST2     | 26      |              |
| ST3     | 27      |              |
| ST4     | 28      |              |
| ST5     | 29      |              |
| ST6     | 30      |              |
| STX     | 31      |              |
| STJ     | 32      |              |
| STZ     | 33      |              |
| JBUS     | 34      |              |
| IOC     | 35      |              |
| IN     | 36      |              |
| OUT     | 37      |              |
| JRED     | 38      |              |
| JMP, JSJ, JOV, JNOV     | 39      |              |
| JA     | 40      |              |
| J1     | 41      |              |
| J2     | 42      |              |
| J3     | 43      |              |
| J4     | 44      |              |
| J5     | 45      |              |
| J6     | 46      |              |
| JX     | 47      |              |
| INCA, DECA, ENTA, ENNA     | 48      |              |
| INC1, DEC1, ENT1, ENN1     | 49      |              |
| INC2, DEC2, ENT2, ENN2     | 50      |              |
| INC3, DEC3, ENT3, ENN3     | 51      |              |
| INC4, DEC4, ENT4, ENN4     | 52      |              |
| INC5, DEC5, ENT5, ENN5    | 53      |              |
| INC6, DEC6, ENT6, ENN6    | 54      |              |
| INCX, DECX, ENTX, ENNX      | 55      |              |
| CMPA, FCMP     | 56      |              |
| CMP1     | 57      |              |
| CMP2     | 58      |              |
| CMP3     | 59      |              |
| CMP4     | 60      |              |
| CMP5     | 61      |              |
| CMP6     | 62      |              |
| CMPX     | 63      |              |
