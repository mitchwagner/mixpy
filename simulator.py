'''
Simulate a MIX computer.
'''

from typing import List, Tuple, NewType, Optional
from enum import Enum

# A "byte" must be capable of holding between 64 and 100 distinct
# values.
BYTE_MIN = 64
BYTE_MAX = 100

# MIX operations are concerned with the value of a MIX byte: the
# details of the implementation are transparent as far as a MIX
# programmer is concerned.
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


class Register:
    '''
    Registers consist of two bytes and a sign
    '''
    sign: Sign
    value: int

    def __init__(self):
        self.sign = Sign.POS
        self.value = 0


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
    _block_size = 14


class PaperTape(IODevice):
    _block_size = 14 


class UndefinedRegisterException(Exception):
   pass


class Simulator:
    '''
    Provides a virtual MIX computer.
    '''
    rA: Register 
    rX: Register 

    i1: Register 
    i2: Register 
    i3: Register 
    i4: Register 
    i5: Register
    i6: Register

    rJ: Register

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

    byte_size: int
    overflow_toggle: bool 
    is_halted: bool
    comparison_indicator: Comparison 

    time = 0


    def __init__(self, byte_size=64):
        '''
        Initialize the MIX computer.

        :param byte_size: Size of a byte (in binary bits)
        '''
        self.byte_size = byte_size 

        self.init_machine()


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
        Initialize machine registers. All registers have a sign bit,
        though the J-register behaves as though its sign bit is always
        positive.

        The A and X registers are both five bytes wide; the remaining
        registers are two bytes wide.
        '''
        self.rA = Word()
        self.rX = Word()

        self.r1 = Word()
        self.r2 = Word()
        self.r3 = Word()
        self.r4 = Word()
        self.r5 = Word()
        self.r6 = Word()

        self.rJ = Word()
        self.rP = Word()


    def attach_IO_device(self, unit_num: int , device: IODevice):
        '''
        :param unit_num: the unit port to attach the device to
        :param device: the device instance to attach to the simulator 
        '''
        None
        

    def detach_IO_device(self, unit_num): 
        None


    def start(self, input_device=16):
        '''
        Loads a boot sequence from the specified input device
        '''
        # Run the boot sequence
            # Load a single memory unit from the specified storage device
            # into memory
            # set Jump location
            # begin 

        self.cycle()


    def _get_bytes(self, value):
        quotients = []
        remainders = []

        # Full words are five bytes long
        for i in range(5):
            quotients.append(value)
            value = value // self.byte_size

        quotients.reverse()

        for q in quotients:
            remainders.append(q % self.byte_size)

        return remainders

    
    def get_field_val(self, start, end, word):
        start = start - 1

        bs = self._get_bytes(word.value)
        bs = bs[start:end]

        num = 0
        place = 0
        for b in reversed(bs):
            num = num + b * self.byte_size ** place
            place += 1
        
        return num
    

    def cycle(self):
        # TODO: track/increment time

        while not self.is_halted:
            i = self.get_next_instruction()
            self.instruction_dispatch(i)


    def get_next_instruction(self):
        '''
        Gets the next instruction, and increments the program counter
        '''
        i: Word = self.memory[self.rP.value]
        self.rP.value += 1
        return i 


    def parse_instruction(self, instruction: Word):
        sign = instruction.sign 
        A = self.get_field_val(1, 2, instruction)
        I = self.get_field_val(3, 3, instruction)
        F = self.get_field_val(4, 4, instruction)
        C = self.get_field_val(5, 5, instruction)

        return ({'sign':sign, 'A':A, 'I':I, 'F':F, 'C':C})


    def get_field(self, F) -> Tuple[int, int]:
        return (F // 8, F % 8)


    def instruction_dispatch(instruction: Word):
        parts = parse_instruction(instruction)
        sign = parts['sign']
        A = parts['A']
        I = parts['I']
        F = get_field(parts['F'])
        C = parts['C']

        address = A.value * sign.value

        if I == 1:
            address += i1.value

        elif I == 2:
            address += i2.value

        elif I == 3:
            address += i3.value

        elif I == 4:
            address += i4.value

        elif I == 5:
            address += i5.value

        elif I == 6:
            address += i6.value

        # TODO: Check for overflow and throw error if it occurs

        self.instr_map[C](address=address, F=F)


    def LDA(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.rA.sign = word.sign
        else:
            self.rA.sign = Sign.POS

        self.rA.value = self.get_field_val(F[0], F[1], word)


    def LD1(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i1.sign = word.sign
        else:
            self.i1.sign = Sign.POS

        self.i1.value = self.get_field_val(F[0], F[1], word)



    def LD2(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i2.sign = word.sign
        else:
            self.i2.sign = Sign.POS

        self.i2.value = self.get_field_val(F[0], F[1], word)


    def LD3(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i3.sign = word.sign
        else:
            self.i3.sign = Sign.POS

        self.i3.value = self.get_field_val(F[0], F[1], word)


    def LD4(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i4.sign = word.sign
        else:
            self.i4.sign = Sign.POS

        self.i4.value = self.get_field_val(F[0], F[1], word)


    def LD5(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i5.sign = word.sign
        else:
            self.i5.sign = Sign.POS

        self.i5.value = self.get_field_val(F[0], F[1], word)


    def LD6(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.i6.sign = word.sign
        else:
            self.i6.sign = Sign.POS

        self.i6.value = self.get_field_val(F[0], F[1], word)


    def LDX(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            self.rX.sign = word.sign
        else:
            self.rX.sign = Sign.POS

        self.rX.value = self.get_field_val(F[0], F[1], word)


    def LDAN(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.rA.sign = Sign.NEG
            else:
                self.rA.sign = Sign.POS
        else:
            self.rA.sign = Sign.NEG

        self.rA.value = self.get_field_val(F[0], F[1], word)


    def LDXN(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.rX.sign = Sign.NEG
            else:
                self.rX.sign = Sign.POS
        else:
            self.rX.sign = Sign.NEG

        self.rX.value = self.get_field_val(F[0], F[1], word)


    def LD1N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i1.sign = Sign.NEG
            else:
                self.i1.sign = Sign.POS
        else:
            self.i1.sign = Sign.NEG

        self.i1.value = self.get_field_val(F[0], F[1], word)


    def LD2N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i2.sign = Sign.NEG
            else:
                self.i2.sign = Sign.POS
        else:
            self.i2.sign = Sign.NEG

        self.i2.value = self.get_field_val(F[0], F[1], word)


    def LD3N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i3.sign = Sign.NEG
            else:
                self.i3.sign = Sign.POS
        else:
            self.i3.sign = Sign.NEG

        self.i3.value = self.get_field_val(F[0], F[1], word)


    def LD4N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i4.sign = Sign.NEG
            else:
                self.i4.sign = Sign.POS
        else:
            self.i4.sign = Sign.NEG

        self.i4.value = self.get_field_val(F[0], F[1], word)


    def LD5N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i5.sign = Sign.NEG
            else:
                self.i5.sign = Sign.POS
        else:
            self.i5.sign = Sign.NEG

        self.i5.value = self.get_field_val(F[0], F[1], word)


    def LD6N(self, address, F):
        word = self.memory[address] 

        use_sign = False
        if F[0] == 0:
            F = (1, F[1])
            use_sign = True
        
        if use_sign:
            if word.sign == Sign.POS:
                self.i6.sign = Sign.NEG
            else:
                self.i6.sign = Sign.POS
        else:
            self.i6.sign = Sign.NEG

        self.i6.value = self.get_field_val(F[0], F[1], word)


    def STA(self):
        raise NotImplementedError 


    def STX(self):
        raise NotImplementedError 


    def ST1(self):
        raise NotImplementedError 


    def ST2(self):
        raise NotImplementedError 


    def ST3(self):
        raise NotImplementedError 


    def ST4(self):
        raise NotImplementedError 


    def ST5(self):
        raise NotImplementedError 


    def ST6(self):
        raise NotImplementedError 


    def STJ(self):
        raise NotImplementedError 


    def STZ(self, address, F):
        raise NotImplementedError 


    # TODO: Overflow
    def ADD(self, address, F):
        '''
        Add the field from the specified address to register A
        '''
        word = self.memory[address] 

        use_sign = False
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


    # TODO: Overflow
    def SUB(self, address, F):
        '''
        Subtract the field from the specified address to register A
        '''
        word = self.memory[address] 

        use_sign = False
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

    # TODO: Overflow
    def MUL(self, address, F):
        raise NotImplementedError 


    def DIV(self, address, F):
        raise NotImplementedError 


    def ENTA(self, address, F):
        raise NotImplementedError 


    def ENTX(self, address, F):
        raise NotImplementedError 


    def ENTi(self, address, F):
        raise NotImplementedError 


    def ENNA(self):
        raise NotImplementedError 


    def ENNi(self, i):
        raise NotImplementedError 


    def INCA(self):
        raise NotImplementedError 


    def INCX(self):
        raise NotImplementedError 


    def INCi(self, i):
        raise NotImplementedError 


    def DECA(self):
        raise NotImplementedError 


    def DECX(self):
        raise NotImplementedError 


    def DECi(self, i):
        raise NotImplementedError 

    
    def CMPA(self):
        raise NotImplementedError 


    def CMPX(self):
        raise NotImplementedError 


    def CMP1(self, i):
        raise NotImplementedError 


    def CMP2(self, i):
        raise NotImplementedError 


    def CMP3(self, i):
        raise NotImplementedError 


    def CMP4(self, i):
        raise NotImplementedError 


    def CMP5(self, i):
        raise NotImplementedError 


    def CMP6(self, i):
        raise NotImplementedError 


    def JUMPA(self):
        raise NotImplementedError 
        

    def JUMP1(self, i):
        raise NotImplementedError 


    def JUMP2(self, i):
        raise NotImplementedError 


    def JUMP3(self, i):
        raise NotImplementedError 


    def JUMP4(self, i):
        raise NotImplementedError 


    def JUMP5(self, i):
        raise NotImplementedError 


    def JUMP6(self, i):
        raise NotImplementedError 


    def JUMPX(self, ):
        raise NotImplementedError 


    def JMP(self):
        raise NotImplementedError 


    def JSJ(self):
        raise NotImplementedError 


    def JOV(self):
        raise NotImplementedError 


    def JNOV(self):
        raise NotImplementedError 


    def JL(self):
        raise NotImplementedError 


    def JE(self):
        raise NotImplementedError 


    def JG(self):
        raise NotImplementedError 


    def JGE(self):
        raise NotImplementedError 

         
    def JNE(self):
        raise NotImplementedError 


    def JLE(self):
        raise NotImplementedError 


    def JAN(self):
        raise NotImplementedError 


    def JAZ(self):
        raise NotImplementedError 


    def JAP(self):
        raise NotImplementedError 


    def JANN(self):
        raise NotImplementedError 


    def JANZ(self):
        raise NotImplementedError 


    def JANP(self):
        raise NotImplementedError 


    def JXN(self):
        raise NotImplementedError 


    def JXZ(self):
        raise NotImplementedError 


    def JXP(self):
        raise NotImplementedError 


    def JXNN(self):
        raise NotImplementedError 


    def JXNZ(self):
        raise NotImplementedError 


    def JXNP(self):
        raise NotImplementedError 


    def JiN(self, i):
        raise NotImplementedError 


    def JiZ(self, i):
        raise NotImplementedError 


    def JiP(self, i):
        raise NotImplementedError 


    def JiNN(self, i):
        raise NotImplementedError 


    def JiNZ(self, i):
        raise NotImplementedError 


    def JiNP(self, i):
        raise NotImplementedError 


    def SLA(self):
        raise NotImplementedError 


    def SRA(self):
        raise NotImplementedError 


    def SLAX(self):
        raise NotImplementedError 


    def SRAX(self):
        raise NotImplementedError 


    def SLC(self):
        raise NotImplementedError 


    def SRC(self):
        raise NotImplementedError 


    def MOVE(self):
        raise NotImplementedError 


    def NOP(self):
        '''
        Do nothing
        '''
        None


    def HLT(self):
        '''
        Pauses a machine; when restarted, the effect is equivalent to
        a NOP instruction.
        '''
        self.is_halted = True


    def restart(self):
        '''
        Restart a halted machine
        '''
        self.is_halted = False
        self.cycle()


    def IN(self):
        raise NotImplementedError 


    def OUT(self):
        raise NotImplementedError 


    def IOC(self):
        raise NotImplementedError 


    def JRED(self):
        raise NotImplementedError 


    def JBUS(self):
        raise NotImplementedError 


    def NUM(self):
        raise NotImplementedError 


    def CHAR(self):
        raise NotImplementedError 

    # Map instruction codes to the function implementing each instruction
    instr_map = {
        0: NOP,
        1: ADD,
        2: SUB,
        3: MUL,
        4: DIV,
        5: None, # This maps to num, char, and halt
        6: None, # This maps to shift (sla, sra, slax, srax, slc, src
        7: MOVE,
        8: LDA,
        9: LD1,
        10: LD2,
        11: LD3,
        12: LD4,
        13: LD5,
        14: LD6,
        15: LDX,
        16: LDAN,
        17: LD1N,
        18: LD2N,
        19: LD3N,
        20: LD4N,
        21: LD5N,
        22: LD6N,
        23: LDXN,
        24: STA,
        25: ST1,
        26: ST2,
        27: ST3,
        28: ST4,
        29: ST5,
        30: ST6,
        31: STX,
        32: STJ,
        33: STZ,
        34: JBUS,
        35: IOC,
        36: IN,
        37: OUT,
        38: JRED,
        39: None, # This maps to various jump instructions
        40: JUMPA,
        41: JUMP1,
        42: JUMP2,
        43: JUMP3,
        44: JUMP4,
        45: JUMP5,
        46: JUMP6,
        47: JUMPX, 
        48: None, # Maps to INCA, DECA, ENTA, ENNA
        49: None, # Maps to INCi, DECi, ENTi, and ENNi
        50: None, # Maps to INCi, DECi, ENTi, and ENNi
        51: None, # Maps to INCi, DECi, ENTi, and ENNi
        52: None, # Maps to INCi, DECi, ENTi, and ENNi
        53: None, # Maps to INCi, DECi, ENTi, and ENNi
        54: None, # Maps to INCi, DECi, ENTi, and ENNi
        55: None, # Maps to INCX, DECX, ENTX, ENNX
        56: CMPA,
        57: CMP1,
        58: CMP2,
        59: CMP3,
        60: CMP4,
        61: CMP5,
        62: CMP6,
        63: CMPX
    }

    # Map instruction codes to the length of time each instruction takes
    time_map = {
        0: 1,
        1: 2,
        2: 2,
        3: 10,
        4: 12,
        5: 10,
        6: 2,
        7: 1, # TODO: Special
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 2,
        13: 2,
        14: 2,
        15: 2,
        16: 2,
        17: 2,
        18: 2,
        19: 2,
        20: 2,
        21: 2,
        22: 2,
        23: 2,
        24: 2,
        25: 2,
        26: 2,
        27: 2,
        28: 2,
        29: 2,
        30: 2,
        31: 2,
        32: 2,
        33: 2,
        34: 1,
        35: 1, # TODO: Special
        36: 1, # TODO: Special
        37: 1, # TODO: Special
        38: 1,
        39: 1,
        40: 1,
        41: 1,
        42: 1,
        43: 1,
        44: 1,
        45: 1,
        46: 1,
        47: 1,
        48: 1,
        49: 1,
        50: 1,
        51: 1,
        52: 1,
        53: 1,
        54: 1,
        55: 1,
        56: 2,
        57: 2,
        58: 2,
        59: 2,
        60: 2,
        61: 2,
        62: 2,
        63: 2 
    }
