#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC5: A 5-stage Pipelined RISC-V ISA Simulator
#
#   Constant definitions
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


import numpy as np

#--------------------------------------------------------------------------
#   Data types & basic constants
#--------------------------------------------------------------------------

WORD                = np.uint32
SWORD               = np.int32

Y                   = True
N                   = False

#--------------------------------------------------------------------------
#   RISC-V constants
#--------------------------------------------------------------------------

WORD_SIZE           = 4
NUM_REGS            = 32

BUBBLE              = WORD(0x00004033)      # Machine-generated NOP:  xor x0, x0, x0
NOP                 = WORD(0x00000013)      # Software-generated NOP: addi zero, zero, 0
ILLEGAL             = WORD(0xffffffff)

OP_MASK             = WORD(0x0000007f)
OP_SHIFT            = 0
RD_MASK             = WORD(0x00000f80)
RD_SHIFT            = 7
FUNCT3_MASK         = WORD(0x00007000)
FUNCT3_SHIFT        = 12
RS1_MASK            = WORD(0x000f8000)
RS1_SHIFT           = 15
RS2_MASK            = WORD(0x01f00000)
RS2_SHIFT           = 20
FUNCT7_MASK         = WORD(0xfe000000)
FUNCT7_SHIFT        = 25


#--------------------------------------------------------------------------
#   ISA table index
#--------------------------------------------------------------------------

IN_NAME             = 0
IN_MASK             = 1
IN_TYPE             = 2
IN_CLASS            = 3


#--------------------------------------------------------------------------
#   ISA table[IN_TYPE]: Instruction types for disassembling
#--------------------------------------------------------------------------

R_TYPE              = 0
I_TYPE              = 1
IL_TYPE             = 2     # I_TYPE, but load instruction
IJ_TYPE             = 3     # I_TYPE, but jalr instruction
IS_TYPE             = 4     # I_TYPE, but shift instructions
U_TYPE              = 5
S_TYPE              = 6
B_TYPE              = 7
J_TYPE              = 8
X_TYPE              = 9


#--------------------------------------------------------------------------
#   ISA table[IN_CLASS]: Instruction classes for collecting stats
#--------------------------------------------------------------------------

CL_ALU              = 0
CL_MEM              = 1
CL_CTRL             = 2


#--------------------------------------------------------------------------
#   PC select signal
#--------------------------------------------------------------------------

PC_4                = 0         # PC + 4
PC_BRJMP            = 1         # branch or jump target
PC_JALR             = 2         # jump register target


#--------------------------------------------------------------------------
#   Control signal (csignal) table index
#--------------------------------------------------------------------------

CS_VAL_INST         = 0
CS_BR_TYPE          = 1
CS_OP1_SEL          = 2
CS_OP2_SEL          = 3
CS_RS1_OEN          = 4
CS_RS2_OEN          = 5
CS_ALU_FUN          = 6
CS_WB_SEL           = 7
CS_RF_WEN           = 8
CS_MEM_EN           = 9
CS_MEM_FCN          = 10
CS_MSK_SEL          = 11


#--------------------------------------------------------------------------
#   csignal[CS_BR_TYPE]: Branch type signal
#--------------------------------------------------------------------------

BR_N                = 0         # Next
BR_NE               = 1         # Branch on NotEqual
BR_EQ               = 2         # Branch on Equal
BR_GE               = 3         # Branch on Greater/Equal
BR_GEU              = 4         # Branch on Greater/Equal Unsigned
BR_LT               = 5         # Branch on Less Than
BR_LTU              = 6         # Branch on Less Than Unsigned
BR_J                = 7         # Jump
BR_JR               = 8         # Jump Register


#--------------------------------------------------------------------------
#   csignal[CS_OP1_SEL]: RS1 operand select signal
#--------------------------------------------------------------------------

OP1_RS1             = 0         # Register source #1 (rs1)
OP1_PC              = 2
OP1_X               = 0


#--------------------------------------------------------------------------
#   csignal[CS_OP2_SEL]: RS2 operand select signal
#--------------------------------------------------------------------------

OP2_RS2             = 0         # Register source #2 (rs2)
OP2_IMI             = 1         # Immediate, I-type
OP2_IMS             = 2         # Immediate, S-type
OP2_IMU             = 3         # Immediate, U-type
OP2_IMJ             = 4         # Immediate, UJ-type
OP2_IMB             = 5         # Immediate, SB-type
OP2_X               = 0


#--------------------------------------------------------------------------
#   csignal[CS_RS1_OEN, CS_RS2_OEN]: Operand enable signal
#--------------------------------------------------------------------------

OEN_0               = 0
OEN_1               = 1


#--------------------------------------------------------------------------
#   csignal[CS_ALU_FUN]: ALU operation signal
#--------------------------------------------------------------------------

ALU_ADD             = 1
ALU_SUB             = 2
ALU_SLL             = 3
ALU_SRL             = 4
ALU_SRA             = 5
ALU_AND             = 6
ALU_OR              = 7
ALU_XOR             = 8
ALU_SLT             = 9
ALU_SLTU            = 10
ALU_COPY1           = 11
ALU_COPY2           = 12
ALU_SEQ             = 13        # Set if equal
ALU_X               = 0


#--------------------------------------------------------------------------
#   csignal[CS_WB_SEL]: Writeback select signal
#--------------------------------------------------------------------------

WB_ALU              = 0         # ALU output
WB_MEM              = 1         # memory output
WB_PC4              = 2         # PC + 4
WB_X                = 0


#--------------------------------------------------------------------------
#   csignal[CS_RF_WEN]: Register file write enable signal
#--------------------------------------------------------------------------

REN_0               = False
REN_1               = True
REN_X               = False


#--------------------------------------------------------------------------
#   csignal[CS_MEM_EN]: Memory enable signal
#--------------------------------------------------------------------------

MEN_0               = False
MEN_1               = True
MEN_X               = False


#--------------------------------------------------------------------------
#   csignal[CS_MEM_FCN]: Memory function type signal
#--------------------------------------------------------------------------

M_XRD               = 0         # load
M_XWR               = 1         # store
M_X                 = 0


#--------------------------------------------------------------------------
#   csignal[CS_MSK_SEL]: Memory mask type select signal
#--------------------------------------------------------------------------

MT_X                = 0         
MT_B                = 1         # byte
MT_H                = 2         # halfword
MT_W                = 3         # word
MT_D                = 4         # doubleword
MT_BU               = 5         # byte (unsigned)
MT_HU               = 6         # halfword (unsigned)
MT_WU               = 7         # word (unsigned)


#--------------------------------------------------------------------------
#   Exceptions
#--------------------------------------------------------------------------

# Multiple exceptions can occur. So they should be a bit vector.
EXC_NONE            = 0         # EXC_NONE should be zero
EXC_IMEM_ERROR      = 1
EXC_DMEM_ERROR      = 2
EXC_ILLEGAL_INST    = 4
EXC_EBREAK          = 8

EXC_MSG = {         EXC_IMEM_ERROR:     "imem access error", 
                    EXC_DMEM_ERROR:     "dmem access error",
                    EXC_ILLEGAL_INST:   "illegal instruction",
                    EXC_EBREAK:         "ebreak",
          }

# Forwarding source
FWD_NONE            = 0
FWD_EX              = 1
FWD_MM              = 2
FWD_WB              = 3
# For 3-stage
FWD_MW              = 4


