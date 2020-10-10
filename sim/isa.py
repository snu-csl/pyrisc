#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   Binary encoding/decoding of RISC-V instructions
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


from consts import *


#--------------------------------------------------------------------------
#   Instruction encodings
#--------------------------------------------------------------------------

LW          = WORD(0b00000000000000000010000000000011)
SW          = WORD(0b00000000000000000010000000100011)
AUIPC       = WORD(0b00000000000000000000000000010111)
LUI         = WORD(0b00000000000000000000000000110111)
ADDI        = WORD(0b00000000000000000000000000010011)

SLLI        = WORD(0b00000000000000000001000000010011)
SLTI        = WORD(0b00000000000000000010000000010011)
SLTIU       = WORD(0b00000000000000000011000000010011)
XORI        = WORD(0b00000000000000000100000000010011)
SRLI        = WORD(0b00000000000000000101000000010011)

SRAI        = WORD(0b01000000000000000101000000010011)
ORI         = WORD(0b00000000000000000110000000010011)
ANDI        = WORD(0b00000000000000000111000000010011)
ADD         = WORD(0b00000000000000000000000000110011)
SUB         = WORD(0b01000000000000000000000000110011)

SLL         = WORD(0b00000000000000000001000000110011)
SLT         = WORD(0b00000000000000000010000000110011)
SLTU        = WORD(0b00000000000000000011000000110011)
XOR         = WORD(0b00000000000000000100000000110011)
SRL         = WORD(0b00000000000000000101000000110011)

SRA         = WORD(0b01000000000000000101000000110011)
OR          = WORD(0b00000000000000000110000000110011)
AND         = WORD(0b00000000000000000111000000110011)
JALR        = WORD(0b00000000000000000000000001100111)
JAL         = WORD(0b00000000000000000000000001101111)

BEQ         = WORD(0b00000000000000000000000001100011)
BNE         = WORD(0b00000000000000000001000001100011)
BLT         = WORD(0b00000000000000000100000001100011)
BGE         = WORD(0b00000000000000000101000001100011)
BLTU        = WORD(0b00000000000000000110000001100011)

BGEU        = WORD(0b00000000000000000111000001100011)
ECALL       = WORD(0b00000000000000000000000001110011)
EBREAK      = WORD(0b00000000000100000000000001110011)


#--------------------------------------------------------------------------
#   Instruction masks
#--------------------------------------------------------------------------

LW_MASK     = WORD(0b00000000000000000111000001111111)
SW_MASK     = WORD(0b00000000000000000111000001111111)
AUIPC_MASK  = WORD(0b00000000000000000000000001111111)
LUI_MASK    = WORD(0b00000000000000000000000001111111)
ADDI_MASK   = WORD(0b00000000000000000111000001111111)

SLLI_MASK   = WORD(0b11111100000000000111000001111111)
SLTI_MASK   = WORD(0b00000000000000000111000001111111)
SLTIU_MASK  = WORD(0b00000000000000000111000001111111)
XORI_MASK   = WORD(0b00000000000000000111000001111111)
SRLI_MASK   = WORD(0b11111100000000000111000001111111)

SRAI_MASK   = WORD(0b11111100000000000111000001111111)
ORI_MASK    = WORD(0b00000000000000000111000001111111)
ANDI_MASK   = WORD(0b00000000000000000111000001111111)
ADD_MASK    = WORD(0b11111110000000000111000001111111)
SUB_MASK    = WORD(0b11111110000000000111000001111111)

SLL_MASK    = WORD(0b11111110000000000111000001111111)
SLT_MASK    = WORD(0b11111110000000000111000001111111)
SLTU_MASK   = WORD(0b11111110000000000111000001111111)
XOR_MASK    = WORD(0b11111110000000000111000001111111)
SRL_MASK    = WORD(0b11111110000000000111000001111111)

SRA_MASK    = WORD(0b11111110000000000111000001111111)
OR_MASK     = WORD(0b11111110000000000111000001111111)
AND_MASK    = WORD(0b11111110000000000111000001111111)
JALR_MASK   = WORD(0b00000000000000000111000001111111)
JAL_MASK    = WORD(0b00000000000000000000000001111111)

BEQ_MASK    = WORD(0b00000000000000000111000001111111)
BNE_MASK    = WORD(0b00000000000000000111000001111111)
BLT_MASK    = WORD(0b00000000000000000111000001111111)
BGE_MASK    = WORD(0b00000000000000000111000001111111)
BLTU_MASK   = WORD(0b00000000000000000111000001111111)

BGEU_MASK   = WORD(0b00000000000000000111000001111111)
ECALL_MASK  = WORD(0b11111111111111111111111111111111)
EBREAK_MASK = WORD(0b11111111111111111111111111111111)


#--------------------------------------------------------------------------
#   ISA table
#--------------------------------------------------------------------------

isa         = { 
    LW      : [ "lw",       LW_MASK,    IL_TYPE, CL_MEM,  OP1_RS1, OP2_IMI, MEM_LD,   MT_W,  ],
    SW      : [ "sw",       SW_MASK,    S_TYPE,  CL_MEM,  OP1_RS1, OP2_IMS, MEM_ST,   MT_W,  ],
    AUIPC   : [ "auipc",    AUIPC_MASK, U_TYPE,  CL_ALU,  OP1_PC,  OP2_IMU, ALU_ADD,  MT_X,  ],
    LUI     : [ "lui",      LUI_MASK,   U_TYPE,  CL_ALU,  OP1_X,   OP2_IMU, ALU_ADD,  MT_X,  ],
    ADDI    : [ "addi",     ADDI_MASK,  I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_ADD,  MT_X,  ],

    SLLI    : [ "slli",     SLLI_MASK,  IS_TYPE, CL_ALU,  OP1_RS1, OP2_IMI, ALU_SLL,  MT_X,  ],
    SLTI    : [ "slti",     SLTI_MASK,  I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_SLT,  MT_X,  ],
    SLTIU   : [ "sltiu",    SLTIU_MASK, I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_SLTU, MT_X,  ],
    XORI    : [ "xori",     XORI_MASK,  I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_XOR,  MT_X,  ],
    SRLI    : [ "srli",     SRLI_MASK,  IS_TYPE, CL_ALU,  OP1_RS1, OP2_IMI, ALU_SRL,  MT_X,  ],

    SRAI    : [ "srai",     SRAI_MASK,  IS_TYPE, CL_ALU,  OP1_RS1, OP2_IMI, ALU_SRA,  MT_X,  ],
    ORI     : [ "ori",      ORI_MASK,   I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_OR,   MT_X,  ],
    ANDI    : [ "andi",     ANDI_MASK,  I_TYPE,  CL_ALU,  OP1_RS1, OP2_IMI, ALU_AND,  MT_X,  ],
    ADD     : [ "add",      ADD_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_ADD,  MT_X,  ],
    SUB     : [ "sub",      SUB_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SUB,  MT_X,  ],

    SLL     : [ "sll",      SLL_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SLL,  MT_X,  ],
    SLT     : [ "slt",      SLT_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SLT,  MT_X,  ],
    SLTU    : [ "sltu",     SLTU_MASK,  R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SLTU, MT_X,  ],
    XOR     : [ "xor",      XOR_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_XOR,  MT_X,  ],
    SRL     : [ "srl",      SRL_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SRL,  MT_X,  ],

    SRA     : [ "sra",      SRA_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_SRA,  MT_X,  ],
    OR      : [ "or",       OR_MASK,    R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_OR,   MT_X,  ],
    AND     : [ "and",      AND_MASK,   R_TYPE,  CL_ALU,  OP1_RS1, OP2_RS2, ALU_AND,  MT_X,  ],
    JALR    : [ "jalr",     JALR_MASK,  IJ_TYPE, CL_CTRL, OP1_RS1, OP2_IMI, ALU_ADD,  MT_X,  ],
    JAL     : [ "jal",      JAL_MASK,   J_TYPE,  CL_CTRL, OP1_RS1, OP2_IMJ, ALU_X,    MT_X,  ],

    BEQ     : [ "beq",      BEQ_MASK,   B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],
    BNE     : [ "bne",      BNE_MASK,   B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],
    BLT     : [ "blt",      BLT_MASK,   B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],
    BGE     : [ "bge",      BGE_MASK,   B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],
    BLTU    : [ "bltu",     BLTU_MASK,  B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],

    BGEU    : [ "bgeu",     BGEU_MASK,  B_TYPE,  CL_CTRL, OP1_RS1, OP2_IMB, ALU_X,    MT_X,  ],
    ECALL   : [ "ecall",    ECALL_MASK, X_TYPE,  CL_CTRL, OP1_X,   OP2_X,   ALU_X,    MT_X,  ],
    EBREAK  : [ "ebreak",   EBREAK_MASK,X_TYPE,  CL_CTRL, OP1_X,   OP2_X,   ALU_X,    MT_X,  ],
}


#--------------------------------------------------------------------------
#   RISCV: decodes RISC-V instructions
#--------------------------------------------------------------------------

class RISCV(object):

    @staticmethod
    def dump():
        for k, v in isa.items():
            print("%s 0x%08x" % (v[0], k))

    @staticmethod
    def opcode(inst):
        for k, v in isa.items():
            if not (inst & v[IN_MASK]) ^ k:
                return k
        return ILLEGAL

    @staticmethod
    def opcode_name(opcode):
        return isa[opcode][IN_NAME]

    @staticmethod
    def rs1(inst):
        return (inst & RS1_MASK) >> RS1_SHIFT

    @staticmethod
    def rs2(inst):
        return (inst & RS2_MASK) >> RS2_SHIFT

    @staticmethod
    def rd(inst):
        return (inst & RD_MASK) >> RD_SHIFT

    @staticmethod
    def sign_extend(v, n):
        if v >> (n - 1):
            return ((1 << (32 - n)) - 1) << n | v
        else:
            return v

    @staticmethod
    def imm_i(inst):
        imm     = (inst >> 20) & 0xfff
        return RISCV.sign_extend(imm, 12)

    @staticmethod
    def imm_u(inst):
        return inst & 0xfffff000

    @staticmethod
    def imm_s(inst):
        imm     = ((inst >> 25) & 0x7f) << 5
        imm     |= ((inst >> 7) & 0x1f)
        return RISCV.sign_extend(imm, 12) 

    @staticmethod
    def imm_b(inst):
        imm     = (inst >> 31) << 11
        imm     |= ((inst >> 7) & 1) << 10
        imm     |= ((inst >> 25) & 0x3f) << 4
        imm     |= (inst >> 8) & 0xf 
        imm     = imm << 1
        return RISCV.sign_extend(imm, 13)

    @staticmethod
    def imm_j(inst):
        imm     = (inst >> 31) << 19
        imm     |= ((inst >> 12) & 0xff) << 11
        imm     |= ((inst >> 20) & 1) << 10
        imm     |= (inst >> 21) & 0x3ff
        imm     = imm << 1
        return RISCV.sign_extend(imm, 21)



