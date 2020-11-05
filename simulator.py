'''
Simulate a MIX computer.
'''

from typing import List, Dict, Tuple, NewType, Optional
from enum import Enum


# A "byte" must be capable of holding between 64 and 100 distinct
# values.
BYTE_MIN = 64
BYTE_MAX = 100


class Sign(Enum):
    '''
    Each register and memory cell has a 1-bit sign indicator
    '''
    POS = 1
    NEG = -1


class Comparison(Enum):
    '''
    Comparison instructions set the comparison indicator to
    one of these three states.
    '''
    LESS = -1
    EQUAL = 0
    GREATER = 1


class Word:
    '''
    A full word consists of a sign bit and five bytes. We can index 
    into a word using field specifications. The first field (0) refers
    to the sign bit. The remaining fields (1:n) refer to the cell's 
    n bytes. In keeping with Knuth's specification, words are
    big-endian.
    '''
    sign: Sign
    value: int

    def __init__(self, value=0):
        self.value = abs(value)
        if value >= 0:
            self.sign = Sign.POS
        if value < 0:
            self.sign = Sign.NEG


# TODO: the J register behaves as if it is always positive.
class Register:
    '''
    There are two register variants: five-byte registers and two-byte
    registers. In addition, every register has a sign (+ or -).
    '''
    sign: Sign
    value: int
    num_bytes: int


    def __init__(self, num_bytes=5):
        self.sign = Sign.POS
        self.value = 0

        # Number of bytes the register comprises 
        self.num_bytes = num_bytes


class IODevice:
    '''
    Abstract class for IO devices.
    '''
    _block_size: int
    num_blocks: int
    blocks: List[Word]

    def __init__(self, num_blocks):
        blocks: List[Word] = [] 

        for block in num_blocks:
            blocks.append(Word())

        self.blocks = blocks


    # TODO: there is a difference between, say, paper tape, which
    # writes out 5 characters at a time, and a disk/drum, which writes
    # out a single word. There may be a need for further subclassing.
    def write_to_file(self, handle):
        None 


class TapeUnit(IODevice):
    _block_size = 100


class DiskUnit(IODevice): 
    _block_size = 100


class CardReader(IODevice):
    _block_size = 16


class CardPunch(IODevice):
    _block_size = 16


class LinePrinter(IODevice):
    _block_size = 24 


class TypewriterTerminal(IODevice):
    '''
    If a typewriter is used for input, the "carriage return" typed at
    the end of each line cuases the remainder of that line to be
    filled with blanks.
    '''
    _block_size = 14


class PaperTape(IODevice):
    _block_size = 14 


class UndefinedRegisterException(Exception):
    '''
    Attempting to use an undefined (index) register 
    '''
    pass


class UndefinedCharacterException(Exception):
    '''
    Erroneous attempt to convert a number, for which no character
    is defined, into a character.
    '''
    pass


class MemoryLimitExceededException(Exception):
    '''
    Reading/writing beyond memory unit boundaries
    '''
    pass


class ByteSizeException(Exception):
    pass


class Simulator:
    '''
    Provides a virtual MIX computer.
    '''
    
    # A dictionary allowing clean lookup of all registers
    registers : Dict[int, Register] 

    # Shorthand variables particular registers 
    rA : Register
    rX : Register
    rJ : Register

    # Tape and disk storage devices read full words (five bytes and a sign)
    tape0: Optional[TapeUnit]
    tape1: Optional[TapeUnit]
    tape2: Optional[TapeUnit]
    tape3: Optional[TapeUnit]
    tape4: Optional[TapeUnit]
    tape5: Optional[TapeUnit]
    tape6: Optional[TapeUnit]
    tape7: Optional[TapeUnit]

    disk0: Optional[DiskUnit]
    disk1: Optional[DiskUnit]
    disk2: Optional[DiskUnit]
    disk3: Optional[DiskUnit]
    disk4: Optional[DiskUnit]
    disk5: Optional[DiskUnit]
    disk6: Optional[DiskUnit]
    disk7: Optional[DiskUnit]

    # These IO devices operate on the basis of character codes:
    # the sign bit of all words is set to "+".
    card_reader: Optional[CardReader]
    card_punch: Optional[CardPunch]
    line_printer: Optional[LinePrinter]
    terminal: Optional[TypewriterTerminal]
    paper_tape: Optional[PaperTape]

    memory: List[Word]

    # Program Counter
    rP: Register   

    max_byte_size: int
    overflow_toggle: bool 
    is_halted: bool
    comparison_indicator: Comparison 

    time = 0

    def __init__(self, max_byte_size=64):
        '''
        Initialize the MIX computer.

        :param byte_size: maximum value of a byte 
        '''
        
        self._set_max_byte_size(max_byte_size)
        self.init_machine()


    def _set_max_byte_size(self, size):
        self._verify_max_byte_size(size)
        self.max_byte_size = size 


    def _verify_max_byte_size(self, size):
        if size < BYTE_MIN or size > BYTE_MAX:
            raise ByteSizeException


    def init_machine(self):
        '''
        Initialize machine hardware.
        '''
        self.overflow_toggle = False
        self.is_halted = False
        self.time = 0
        self.comparison_indicator = Comparison.EQUAL 
        self.init_memory()
        self.init_registers()


    def init_memory(self):
        '''
        Initializes machine memory. A MIX computer provides 4000
        5-byte cells.
        '''
        memory: List[Word] = []

        for i in range(4000):
            memory.append(Word())

        self.memory = memory


    def init_registers(self):
        '''
        Initialize machine registers.
        '''

        self.registers = {
            'A': Register(5),
            'X': Register(5),
            'J': Register(2),
            1 : Register(2),
            2 : Register(2),
            3 : Register(2),
            4 : Register(2),
            5 : Register(2),
            6 : Register(2)
        }

        self.rA = self.registers['A']
        self.rX = self.registers['X']
        self.rJ = self.registers['J']

        self.rP = Word()


    def start(self, boot_device=16):
        '''
        Loads a boot sequence from the specified input device
        '''

        self.boot(boot_device=boot_device)
        self.cycle()

    
    def boot(self, boot_device=16):
        '''
        0) Set J register to 0, and clear the overflow toggle
        1) Read one card into memory, starting at memory location 0000
        2) Once card is loaded, begin execution from 0000
        '''
        None


    def cycle(self):
        '''
        Execute until a halting instruction is processed
        '''
        while not self.is_halted:
            i = self.get_next_instruction()
            parts = self.parse_instruction(i)

            increment_time(parts)
            self.instruction_dispatch(parts)


    def get_next_instruction(self):
        '''
        Gets the next instruction, and increments the program counter
        '''
        i: Word = self.memory[self.rP.value]
        self.rP.value += 1
        return i 


    # TODO: it might be cleaner to make this return an actual type 
    def parse_instruction(self, instruction: Word):
        sign = instruction.sign 
        A = self.get_field_val(1, 2, instruction)
        I = self.get_field_val(3, 3, instruction)
        F = self.get_field_val(4, 4, instruction)
        C = self.get_field_val(5, 5, instruction)

        return ({'sign':sign, 'A':A, 'I':I, 'F':F, 'C':C})

    
    def get_field_val(self, start, end, word):
        '''
        Given a word and a field, return the value stored
        in the specified field.
        '''
        start = start - 1

        bs = self._get_bytes(word.value)
        bs = bs[start:end]

        return self._bytes_to_val(bs)


    # TODO: change to "val_to_bytes"
    def _get_bytes(self, value):
        '''
        Transform a (positive) integer value into a list of bytes 
        '''
        quotients = []
        remainders = []

        # Full words are five bytes long
        for i in range(5):
            quotients.append(value)
            value = value // self.max_byte_size

        quotients.reverse()

        for q in quotients:
            remainders.append(q % self.max_byte_size)

        return remainders


    def _bytes_to_val(self, bs):
        val = 0
        place = 0

        for b in reversed(bs):
            val = val + b * self.max_byte_size ** place
            place += 1

        return val


    def increment_time(self, parsed_instruction) -> None:
        '''
        Increment the total running time of the computer
        '''
        parameter = self.get_time_parameter(parsed_instruction)

        op_code = parsed_instruction['C'] 
        self.time += time_map[op_code](parameter) 


    def get_time_parameter(self, parsed_instruction) -> int:
        '''
        A very few instructions require an amount of time that is a
        function of some variable. This method computes that variable,
        returning -1 in the instances where no variable is necessary.
        '''
        if op_code == 7:
            return parsed_instruction['F']

        # TODO: Implement logic
        elif op_code == 35 or op_code == 36 or op_code == 37:
            return 1000

        else:
            return -1


    def instruction_dispatch(self, parsed_instruction):
        '''
        Select and execute the function implementing the indicated
        instruction
        '''

        sign = parsed_instruction['sign']
        A = parsed_instruction['A']
        I = parsed_instruction['I']
        F = parsed_instructions['F']
        C = parsed_instructions['C']

        address = A.value * sign.value

        address = self.index_from_address(address, I)

        params = {
            'address': address,
            'F': F,
            'C': C
        }

        self.instr_map[C](**params)


    def get_field_specification(self, F) -> Tuple[int, int]:
        return (F // 8, F % 8)


    def index_from_address(self, address, I) -> int:
        # TODO: Check for overflow and throw error if it occurs
        register = self.registers[I]
        address += register.value

        return address


    def attach_IO_device(self, unit_num: int , device: IODevice):
        '''
        :param unit_num: the unit port to attach the device to
        :param device: the device instance to attach to the simulator 
        '''
        None
        

    def detach_IO_device(self, unit_num): 
        '''
        :param unit_num: the port of the unit to detach
        '''
        None


    def LD_dispatch(self, address, F, C) -> None:
        '''
        Execute a LD instruction with the proper register
        '''
        register_map = {
            '8': self.registers['A'],
            '9': self.registers['1'],
            '10': self.registers['2'],
            '11': self.registers['3'],
            '12': self.registers['4'],
            '13': self.registers['5'],
            '14': self.registers['6'],
            '15': self.registers['X']
        }

        LD(register_map[C], address, F)
       

    # TODO: Do we need all parameters (C) here?
    # TODO: We could use kwargs for ultimate flexibility. Investigate
    # whether or not every instruction needs all or the same set of
    # parameters 
    def LD(self, register, address, F) -> None:
        '''
        The contents stored in the specified field of the specified
        memory address are loaded into the specified register.
        '''
        word = self.memory[address]
        use_sign = False

        F = self.get_field_specification(F)

        if F[0] == 0:
            F = (1, F[1])
            use_sign = True

        if use_sign:
            register.sign = word.sign
        else:
            register.sign = Sign.POS

        register.value = self.get_field_val(F[0], F[1], word)


    def LDN_dispatch(self, address, F, C) -> None:
        '''
        Execute a LDN instruction with the proper register
        '''
        register_map = {
            '16': self.registers['A'],
            '17': self.registers['1'],
            '18': self.registers['2'],
            '19': self.registers['3'],
            '20': self.registers['4'],
            '21': self.registers['5'],
            '22': self.registers['6'],
            '23': self.registers['X']
        }

        LDN(register_map[C], address, F)


    def LDN(self, register, address, F) -> None:
        '''
        The negation of the contents stored in the specified field of
        the specified memory address are loaded into the specified
        register.
        '''
        word = self.memory[address] 
        use_sign = False

        F = self.get_field_specification(F)

        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                register.sign = Sign.NEG
            else:
                register.sign = Sign.POS
        else:
            register.sign = Sign.NEG

        register.value = self.get_field_val(F[0], F[1], word)


    def ST_dispatch(self, address, F, C) -> None:
        '''
        Execute a ST instruction with the proper register
        '''
        register_map = {
            '24': self.registers['A'],
            '25': self.registers['1'],
            '26': self.registers['2'],
            '27': self.registers['3'],
            '28': self.registers['4'],
            '29': self.registers['5'],
            '30': self.registers['6'],
            '31': self.registers['X']
        }

        ST(register_map[C], address, F)


    def ST(self, register, address, F) -> None:
        '''
        The contents the specified register replace the specified
        field of the specified address.

        The number of bytes in the field is taken from the right-hand
        portion of the register and shifted left if necessary to be
        inserted in the proper field at the address location.

        When storing from the index registers, Bytes 1, 2, and 3 are
        set to zero. 
        '''

        # 0) Figure out what to do about the sign 
        F = self.get_field_specification(F)

        if F[0] == 0:
            F = (1, F[1])
            self.memory[address].sign = register.sign

        # 1) Get the bytes of the register and memory contents
        reg_bytes = self._get_bytes(register.value)
        mem_bytes = self._get_bytes(self.memory[address].value)
        
        num_bytes_needed = 1 + F[1] - F[0]

        # "Shift" by taking the requisite number of bytes off the back
        reg_bytes = reg_bytes[-1 * num_bytes_needed:]

        # Construct a new value based on the field specification
        new_bytes = \
            mem_bytes[:F[0] - 1] + \
            reg_bytes + \
            mem_bytes[F[1]:]

        # Convert the bytes into a value and store the value
        value = self._bytes_to_val(new_bytes)

        self.memory[address].value = value


    def STJ(self, address, F, C) -> None:
        '''
        Same as ST, except that rJ is stored, and its sign is always
        positive.

        With STJ, the normal field specification for F is (0:2), not
        (0:5)
        '''

        # TODO: Check that field specification is valid (here and
        # elsewhere)
        self.ST(self.rJ, address, F)


    def STZ(self, address, F, C) -> None:
        '''
        Same as ST, except that plus zero is stored. That is, the
        specified field of the specified address is cleared to zero. 
        '''
        zero_reg = Register() 
        self.ST(zero_reg, address, F)


    # TODO: Handle overflow in Register class
    # TODO: Set overflow toggle
    def ADD(self, address, F) -> None:
        '''
        Add the field from the specified address to register A
        '''
        word = self.memory[address] 
        use_sign = False

        F = self.get_field_specification(F)
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True

        addend = self.get_field_val(F[0], F[1], word)

        if use_sign:
            addend = addend * word.sign.value

        self.rA.value = self.rA.value * self.rA.sign.value

        self.rA.value = self.rA.value + addend

        if self.rA.value > 0:
            self.rA.sign = Sign.POS
        elif self.rA.value < 0:
            self.rA.sign = Sign.NEG

        self.rA.value = abs(self.rA.value)


    # TODO: Handle overflow in Register class
    # TODO: Set overflow toggle
    def SUB(self, address, F, C) -> None:
        '''
        Subtract the field from the specified address to register A
        '''
        word = self.memory[address] 
        use_sign = False

        F = self.get_field_specification(F)

        if F[0] == 0:
            F = (1, F[1])
            use_sign = True

        subtrahend = self.get_field_val(F[0], F[1], word)

        if use_sign:
            subtrahend = subtrahend * word.sign.value

        self.rA.value = self.rA.value * self.rA.sign.value

        self.rA.value = self.rA.value + subtrahend 

        if self.rA.value > 0:
            self.rA.sign = Sign.POS
        elif self.rA.value < 0:
            self.rA.sign = Sign.NEG

        self.rA.value = abs(self.rA.value)


    # TODO: Handle overflow in Register class
    # TODO: Set overflow toggle
    def MUL(self, address, F, C) -> None:
        '''
        The 10-byte product (rA * value at address) replaces the
        values stored in registers rA and rX (rA holds the more significant
        bytes). The signs of rA and rX are both set to the signs of
        the product.
        '''
        # First, get the product

        # Then, convert to bytes

        # Then, chop up bytes

        # Then, set values of registers (Register class should handle
        # overflow). If there is overflow, set the overflow toggle.

        # Finally, set signs of registers

        raise NotImplementedError 


    # TODO: Handle overflow in Register class
    # TODO: Set overflow toggle
    def DIV(self, address, F, C) -> None:
        '''
        The value of rA and rX, treated as the 10-byte number rAX with
        the sign of rA, is divided by the value stored in the
        specified address. If the divisor is 0 or if the quotient is
        more than five bytes in magnitude (equivalent to |rA| >=
        |divisor|), the result is undefined and the overflow toggle is
        set. Otherwise, the quotient is placed in rA, and the
        remainder is placed in rX. The sign of rA afterwards is the
        sign of the quotient, and the sign of rX is the previous sign
        of rA.
        '''
        # First,

        raise NotImplementedError 


    # TODO: this F is NOT a field specification
    def address_transfer_dispatch(self, address, F, C):
        register_map = {
            '48': self.registers['A'],
            '49': self.registers[1],
            '50': self.registers[2],
            '51': self.registers[3],
            '52': self.registers[4],
            '53': self.registers[5],
            '54': self.registers[6],
            '55': self.registers['X'],
        }

        operation_map = {
            '0': self.INC,
            '1': self.DEC,
            '2': self.ENT,
            '3': self.ENN,
        }

        register = register_map['C']
        op = operation_map['F']

        op(register, address, F)


    def INC(self, register, address, F) -> None:
        raise NotImplementedError 


    def DEC(self, register, address, F) -> None:
        raise NotImplementedError 


    def ENT(self, register, address, F) -> None:
        raise NotImplementedError 


    def ENN(self, register, address, F) -> None:
        raise NotImplementedError 


    def CMP(self, register, F, C) -> None:
        raise NotImplementedError 


    def CMP_dispatch(self, address, F, C):
        raise NotImplementedError 


    def JUMP(self, register, address, F, C) -> None:
        raise NotImplementedError 


    def JUMP_dispatch(self, address, F, C) -> None:
        # Switch on C to get the register
        # Switch on F to
        raise NotImplementedError 


    def JMP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JSJ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JOV(self, address, F, C) -> None:
        raise NotImplementedError 


    def JNOV(self, address, F, C) -> None:
        raise NotImplementedError 


    def JL(self, address, F, C) -> None:
        raise NotImplementedError 


    def JE(self, address, F, C) -> None:
        raise NotImplementedError 


    def JG(self, address, F, C) -> None:
        raise NotImplementedError 


    def JGE(self, address, F, C) -> None:
        raise NotImplementedError 

         
    def JNE(self, address, F, C) -> None:
        raise NotImplementedError 


    def JLE(self, address, F, C) -> None:
        raise NotImplementedError 


    def JAN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JAZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JAP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JANN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JANZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JANP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXNN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXNZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JXNP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiP(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiNN(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiNZ(self, address, F, C) -> None:
        raise NotImplementedError 


    def JiNP(self, address, F, C) -> None:
        raise NotImplementedError 


    def SLA(self, address, F, C) -> None:
        raise NotImplementedError 


    def SRA(self, address, F, C) -> None:
        raise NotImplementedError 


    def SLAX(self, address, F, C) -> None:
        raise NotImplementedError 


    def SRAX(self, address, F, C) -> None:
        raise NotImplementedError 


    def SLC(self, address, F, C) -> None:
        raise NotImplementedError 


    def SRC(self, address, F, C) -> None:
        raise NotImplementedError 


    def MOVE(self, address, F, C) -> None:
        raise NotImplementedError 


    def NOP(self, address, F, C) -> None:
        '''
        Do nothing
        '''
        None


    def HLT(self, address, F, C) -> None:
        '''
        Pauses a machine; when restarted, the effect is equivalent to
        a NOP instruction.
        '''
        self.is_halted = True


    def restart(self) -> None:
        '''
        Restart a halted machine
        '''
        self.is_halted = False
        self.cycle()


    def IN(self, address, F, C) -> None:
        raise NotImplementedError 


    def OUT(self, address, F, C) -> None:
        raise NotImplementedError 


    def IOC(self, address, F, C) -> None:
        raise NotImplementedError 


    def JRED(self, address, F, C) -> None:
        raise NotImplementedError 


    def JBUS(self, address, F, C) -> None:
        raise NotImplementedError 


    def NUM(self, address, F, C) -> None:
        '''
        Change a character code into a numeric code. 
        
        Registers A and X are assumed to contain a 10-byte number in
        character code; the NUM instruction sets the magnitude of rA
        equal to the numerical value of this number. The value of rX
        and the sign of rA are unchanged. 
        
        Bytes 00, 10, 20, ...  convert to the digit zero; bytes 01,
        11, 21, ... to the digit one; etc. 
        
        Overflow is possible, and in this case, the remainder module
        b^5 is retained, where b is the byte size.
        '''
                
        a_bytes = self._get_bytes(self.rA.value)
        x_bytes = self._get_bytes(self.rX.value)

        num = 0
        power = 0

        for b in a_bytes:
            num = num + b * self.byte_size ** power 
            place += 1

        for b in x_bytes:
            num = num + b * self.byte_size ** power 
            place += 1

        num = num % self.byte_size ** 5


    def CHAR(self) -> None:
        raise NotImplementedError 


    # Map instruction codes to the function implementing each instruction
    instr_map = {
        0: NOP,
        1: ADD,
        2: SUB,
        3: MUL,
        4: DIV,
        5: None, # This maps to num, char, and halt
        6: None, # This maps to shift (sla, sra, slax, srax, slc, src)
        7: MOVE,
        8: LD_dispatch,
        9: LD_dispatch,
        10: LD_dispatch,
        11: LD_dispatch,
        12: LD_dispatch,
        13: LD_dispatch,
        14: LD_dispatch,
        15: LD_dispatch,
        16: LDN_dispatch,
        17: LDN_dispatch,
        18: LDN_dispatch,
        19: LDN_dispatch,
        20: LDN_dispatch,
        21: LDN_dispatch,
        22: LDN_dispatch,
        23: LDN_dispatch,
        24: ST_dispatch,
        25: ST_dispatch,
        26: ST_dispatch,
        27: ST_dispatch,
        28: ST_dispatch,
        29: ST_dispatch,
        30: ST_dispatch,
        31: ST_dispatch,
        32: ST_dispatch,
        33: ST_dispatch,
        34: JBUS,
        35: IOC,
        36: IN,
        37: OUT,
        38: JRED,
        39: None, # This maps to various jump instructions
        40: JUMP_dispatch,
        41: JUMP_dispatch,
        42: JUMP_dispatch,
        43: JUMP_dispatch,
        44: JUMP_dispatch,
        45: JUMP_dispatch,
        46: JUMP_dispatch,
        47: JUMP_dispatch,
        48: address_transfer_dispatch,
        49: address_transfer_dispatch,
        50: address_transfer_dispatch,
        51: address_transfer_dispatch,
        52: address_transfer_dispatch,
        53: address_transfer_dispatch,
        54: address_transfer_dispatch,
        55: address_transfer_dispatch,
        56: CMP_dispatch,
        57: CMP_dispatch,
        58: CMP_dispatch,
        59: CMP_dispatch,
        60: CMP_dispatch,
        61: CMP_dispatch,
        62: CMP_dispatch,
        63: CMP_dispatch
    }

    # Map instruction codes to a function computing the amount of
    # time the instruction will take to execute.
    time_map = {
        0: lambda  _: 1,
        1: lambda  _: 2,
        2: lambda  _: 2,
        3: lambda  _: 10,
        4: lambda  _: 12,
        5: lambda  _: 10,
        6: lambda  _: 2,
        7: lambda  f: 1 + 2*f,
        8: lambda  _: 2,
        9: lambda  _: 2,
        10: lambda _: 2,
        11: lambda _: 2,
        12: lambda _: 2,
        13: lambda _: 2,
        14: lambda _: 2,
        15: lambda _: 2,
        16: lambda _: 2,
        17: lambda _: 2,
        18: lambda _: 2,
        19: lambda _: 2,
        20: lambda _: 2,
        21: lambda _: 2,
        22: lambda _: 2,
        23: lambda _: 2,
        24: lambda _: 2,
        25: lambda _: 2,
        26: lambda _: 2,
        27: lambda _: 2,
        28: lambda _: 2,
        29: lambda _: 2,
        30: lambda _: 2,
        31: lambda _: 2,
        32: lambda _: 2,
        33: lambda _: 2,
        34: lambda _: 1,
        35: lambda t: t + 1, # TODO: t is a device-dependent interlock time
        36: lambda t: t + 1, # TODO: t is a device-dependent interlock time
        37: lambda t: t + 1, # TODO: t is a device-dependent interlock time
        38: lambda _: 1,
        39: lambda _: 1,
        40: lambda _: 1,
        41: lambda _: 1,
        42: lambda _: 1,
        43: lambda _: 1,
        44: lambda _: 1,
        45: lambda _: 1,
        46: lambda _: 1,
        47: lambda _: 1,
        48: lambda _: 1,
        49: lambda _: 1,
        50: lambda _: 1,
        51: lambda _: 1,
        52: lambda _: 1,
        53: lambda _: 1,
        54: lambda _: 1,
        55: lambda _: 1,
        56: lambda _: 2,
        57: lambda _: 2,
        58: lambda _: 2,
        59: lambda _: 2,
        60: lambda _: 2,
        61: lambda _: 2,
        62: lambda _: 2,
        63: lambda _: 2,
    }

    character_code_map = {
        0: ' ',
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
        9: 'I',
        10: 'Δ',
        11: 'J',
        12: 'K',
        13: 'L',
        14: 'M',
        15: 'N',
        16: 'O',
        17: 'P',
        18: 'Q',
        19: 'R',
        20: 'Σ',
        21: 'Π',
        22: 'S',
        23: 'T',
        24: 'U',
        25: 'V',
        26: 'W',
        27: 'X',
        28: 'Y',
        29: 'Z',
        30: '0',
        31: '1',
        32: '2',
        33: '3',
        34: '4',
        35: '5',
        36: '6',
        37: '7',
        38: '8',
        39: '9',
        40: '.',
        41: ',',
        42: '(',
        43: ')',
        44: '+',
        45: '-',
        46: '*',
        47: '/',
        48: '=',
        49: '$',
        50: '<',
        51: '>',
        52: '@',
        53: ';',
        54: ':',
        55: "'",
    }
