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

| Op Code | Name | Description |
| ------- | ---- | ----------- |
| 00      | NOP  | |
| 01      | ADD  | |
| 02      | SUB  | |
| 03      | MUL  | |
| 04      | DIV  | |
| 05      | NUM, CHAR, HLT | |
| 06      | SLA, SRA, SLAX, SRAX, SLC, SRC | |
| 07      | MOVE | |
| 08      | LDA  | |
| 09      | LD1  | |
| 10      | LD2  | |
| 11      | LD3  | |
| 12      | LD4  | |
| 13      | LD5  | |
| 14      | LD6  | |
| 15      | LDX  | |
| 16      | LDAN | |
| 17      | LD1N | |
| 18      | LD2N | |
| 19      | LD3N | |
| 20      | LD4N | |
| 21      | LD5N | |
| 22      | LD6N | |
| 23      | LDXN | |
| 24      | STA  | |
| 25      | ST1  | |
| 26      | ST2  | |
| 27      | ST3  | |
| 28      | ST4  | |
| 29      | ST5  | |
| 30      | ST6  | |
| 31      | STX  | |
| 32      | STJ  | |
| 33      | STZ  | |
| 34      | JBUS | |
| 35      | IOC  | |
| 36      | IN   | |
| 37      | OUT  | |
| 38      | JRED | |
| 39      | JMP, JSJ, JOV, JNOV | |
| 40      | JA   | |
| 41      | J1   | |
| 42      | J2   | |
| 43      | J3   | |
| 44      | J4   | |
| 45      | J5   | |
| 46      | J6   | |
| 47      | JX   | |
| 48      | INCA, DECA, ENTA, ENNA | |
| 49      | INC1, DEC1, ENT1, ENN1 | |
| 50      | INC2, DEC2, ENT2, ENN2 | |
| 51      | INC3, DEC3, ENT3, ENN3 | |
| 52      | INC4, DEC4, ENT4, ENN4 | |
| 53      | INC5, DEC5, ENT5, ENN5 | |
| 54      | INC6, DEC6, ENT6, ENN6 | |
| 55      | INCX, DECX, ENTX, ENNX | |
| 56      | CMPA, FCMP | |
| 57      | CMP1 | |
| 58      | CMP2 | |
| 59      | CMP3 | |
| 60      | CMP4 | |
| 61      | CMP5 | |
| 62      | CMP6 | |
| 63      | CMPX | |
