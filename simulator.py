from typing import List, NewType, Optional
from enum import Enum

# A "byte" must be capable of holding between 64 and 100 distinct 
# values. Presuming a base-2 computer, this corresponds to between 6- 
# and 10-bit "bytes".
MIN_BYTE_SIZE = 6
MAX_BYTE_SIZE = 10

# MIX operations are concerned with the value of a MIX byte: the
# details of the implementation are transparent as far as a MIX
# programmer is concerned.
Byte = NewType('Byte', int)


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


class MemoryCell:
    ''' 
    A memory cell consists of a sign bit and a sequence of bytes. We
    can index into a cell using field specifications. The first field
    (0) refers to the sign bit. The remaining fields (1:n) refer to
    the cell's n bytes. In keeping with Knuth's specification, memory
    cells are big-endian.
    ''' 
    sign: Sign 
    bytes: List[Byte]
    num_bytes: int

    def __init__(self, num_bytes): 
        self.sign = Sign.POS
        self.num_bytes = num_bytes
        self.init_bytes(num_bytes)


    def init_bytes(self, num_bytes):
        bytes: List[Byte] = []
        for i in range(num_bytes): 
            bytes.append(Byte(0))

        self.bytes = bytes


    def store(self, field):
        None


    def add(self, field):
        None


    def subtract(self, field):
        None


class StorageDevice:
    block_size: int


class UndefinedRegisterException(Exception):
   pass 


class Simulator:
    '''
    Provides a virtual MIX computer.
    '''
    rA: MemoryCell
    rX: MemoryCell

    i1: MemoryCell
    i2: MemoryCell
    i3: MemoryCell
    i4: MemoryCell
    i5: MemoryCell
    i6: MemoryCell

    rJ: MemoryCell

    tape0: Optional[StorageDevice]
    tape1: Optional[StorageDevice]
    tape2: Optional[StorageDevice]
    tape3: Optional[StorageDevice]
    tape4: Optional[StorageDevice]
    tape5: Optional[StorageDevice]
    tape6: Optional[StorageDevice]
    tape7: Optional[StorageDevice]

    disk8: Optional[StorageDevice]
    disk9: Optional[StorageDevice]
    disk10: Optional[StorageDevice]
    disk11: Optional[StorageDevice]
    disk12: Optional[StorageDevice]
    disk13: Optional[StorageDevice]
    disk14: Optional[StorageDevice]
    disk15: Optional[StorageDevice]

    card_reader: Optional[StorageDevice]
    card_punch: Optional[StorageDevice]
    line_printer: Optional[StorageDevice]
    tt_terminal: Optional[StorageDevice]
    paper_tape: Optional[StorageDevice]

    memory: List[MemoryCell]

    byte_size: int
    overflow_toggle: bool 
    comparison_indicator: Comparison 

    time = 0


    def __init__(self, byte_size=6):
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
        self.comparison_indicator = Comparison.EQUAL 
        self.init_memory()
        self.init_registers()


    def init_memory(self):
        '''
        Initializes machine memory. A MIX computer provides 4000
        5-byte cells.
        '''
        memory: List[MemoryCell] = []

        for i in range(4000):
            memory.append(MemoryCell(5))

        self.memory = memory


    def init_registers(self):
        '''
        Initialize machine registers. All registers have a sign bit, 
        though the J-register behaves as though its sign bit is always
        positive.

        The A and X registers are both five bytes wide; the remaining 
        registers are two bytes wide. 
        '''
        self.rA = MemoryCell(5)
        self.rX = MemoryCell(5)

        self.r1 = MemoryCell(2)
        self.r2 = MemoryCell(2)
        self.r3 = MemoryCell(2)
        self.r4 = MemoryCell(2)
        self.r5 = MemoryCell(2)
        self.r6 = MemoryCell(2)

        self.rJ = MemoryCell(2)


    def run(self):
        # Run the boot sequence
            # Load a single memory unit from the specified storage device
            # into memory
            # Jump to 0 on the tape device
            # begin 

        # Get first instruction
        # Repeat next instruction
        # Where do instructions come from?
        # You parse the instruction to figure out what to do
        #   then, you do it
        None

    
    def get_field_val(self, start, end, cell):
        start = start - 1
        bs = cell.bytes[start:end]

        num = 0
        place = 0
        for b in reversed(bs):
            num = num + b * (2 ** self.byte_size) ** place
            place += 1

        return num * cell.sign.value


    def parse_instruction(self, instruction: MemoryCell):
        sign = instruction.sign 
        A = self.get_field_val(1, 2, instruction)
        I = self.get_field_val(3, 3, instruction)
        F = self.get_field_val(4, 4, instruction)
        C = self.get_field_val(5, 5, instruction)

        return ({'sign':sign, 'A':A, 'I':I, 'F':F, 'C':C})


    def instruction_dispatch(instruction: MemoryCell):
        instr_comps = parse_instruction(instruction)
        code = instr_comps.pop('C')
        instr_map[code]()


    def LDA(self, A, I, F, C):
        raise NotImplementedError 


    def LD1(self, i):
        raise NotImplementedError 


    def LD2(self, i):
        raise NotImplementedError 


    def LD3(self, i):
        raise NotImplementedError 


    def LD4(self, i):
        raise NotImplementedError 


    def LD5(self, i):
        raise NotImplementedError 


    def LD6(self, i):
        raise NotImplementedError 


    def LDX(self):
        raise NotImplementedError 


    def LDAN(self):
        raise NotImplementedError 


    def LDXN(self):
        raise NotImplementedError 


    def LD1N(self, i):
        raise NotImplementedError 


    def LD2N(self, i):
        raise NotImplementedError 


    def LD3N(self, i):
        raise NotImplementedError 


    def LD4N(self, i):
        raise NotImplementedError 


    def LD5N(self, i):
        raise NotImplementedError 


    def LD6N(self, i):
        raise NotImplementedError 


    def STA(self):
        raise NotImplementedError 


    def STX(self):
        raise NotImplementedError 


    def ST1(self, i):
        raise NotImplementedError 


    def ST2(self, i):
        raise NotImplementedError 


    def ST3(self, i):
        raise NotImplementedError 


    def ST4(self, i):
        raise NotImplementedError 


    def ST5(self, i):
        raise NotImplementedError 


    def ST6(self, i):
        raise NotImplementedError 


    def STJ(self):
        raise NotImplementedError 


    def STZ(self):
        raise NotImplementedError 


    def ADD(self):
        raise NotImplementedError 


    def SUB(self):
        raise NotImplementedError 


    def MUL(self):
        raise NotImplementedError 


    def DIV(self):
        raise NotImplementedError 


    def ENTA(self):
        raise NotImplementedError 


    def ENTX(self):
        raise NotImplementedError 


    def ENTi(self, i):
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
        raise NotImplementedError 


    def HLT(self):
        raise NotImplementedError 


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
