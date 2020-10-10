#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
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
#   Data types
#--------------------------------------------------------------------------

WORD                = np.uint32
SWORD               = np.int32


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
#   Memory control signals
#--------------------------------------------------------------------------

M_XRD               = 0
M_XWR               = 1


#--------------------------------------------------------------------------
#   ISA table index
#--------------------------------------------------------------------------

IN_NAME             = 0
IN_MASK             = 1
IN_TYPE             = 2
IN_CLASS            = 3
IN_ALU1             = 4
IN_ALU2             = 5
IN_OP               = 6
IN_MT               = 7


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
#   ISA table[IN_ALU1]: ALU operand select 1
#--------------------------------------------------------------------------

OP1_X               = 0
OP1_RS1             = 1         
OP1_PC              = 2


#--------------------------------------------------------------------------
#   ISA table[IN_ALU2]: ALU operand select 2
#--------------------------------------------------------------------------

OP2_X               = 0
OP2_RS2             = 1         
OP2_IMI             = 2         
OP2_IMS             = 3         
OP2_IMU             = 4
OP2_IMJ             = 5
OP2_IMB             = 6


#--------------------------------------------------------------------------
#   ISA table[IN_OP]: ALU and memory operation control
#--------------------------------------------------------------------------

ALU_X               = 0
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
MEM_LD              = 11
MEM_ST              = 12


#--------------------------------------------------------------------------
#   ISA table[IN_MT]: Memory operation type
#--------------------------------------------------------------------------

MT_X                = 0
MT_B                = 1
MT_H                = 2
MT_W                = 3
MT_D                = 4
MT_BU               = 5
MT_HU               = 6
MT_WU               = 7


#--------------------------------------------------------------------------
#   Exceptions
#--------------------------------------------------------------------------

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

