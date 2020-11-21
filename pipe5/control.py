#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC5: A 5-stage Pipelined RISC-V ISA Simulator
#
#   Pipeline Control logic
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


import sys

from consts import *
from isa import *


#--------------------------------------------------------------------------
#   Control signal table
#--------------------------------------------------------------------------

csignals = {
    LW     : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_ADD  , WB_MEM, REN_1, MEN_1, M_XRD, MT_W, ],
    SW     : [ Y, BR_N  , OP1_RS1, OP2_IMS, OEN_1, OEN_1, ALU_ADD  , WB_X  , REN_0, MEN_1, M_XWR, MT_W, ],
    AUIPC  : [ Y, BR_N  , OP1_PC,  OP2_IMU, OEN_0, OEN_0, ALU_ADD  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    LUI    : [ Y, BR_N  , OP1_X,   OP2_IMU, OEN_0, OEN_0, ALU_COPY2, WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    ADDI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_ADD  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],

    SLLI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_SLL  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SLTI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_SLT  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SLTIU  : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_SLTU , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    XORI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_XOR  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SRLI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_SRL  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],

    SRAI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_SRA  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    ORI    : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_OR   , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    ANDI   : [ Y, BR_N  , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_AND  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    ADD    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_ADD  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SUB    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SUB  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],

    SLL    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SLL  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SLT    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SLT  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SLTU   : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SLTU , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    XOR    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_XOR  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    SRL    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SRL  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],

    SRA    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_SRA  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    OR     : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_OR   , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    AND    : [ Y, BR_N  , OP1_RS1, OP2_RS2, OEN_1, OEN_1, ALU_AND  , WB_ALU, REN_1, MEN_0, M_X  , MT_X, ],
    JALR   : [ Y, BR_JR , OP1_RS1, OP2_IMI, OEN_1, OEN_0, ALU_ADD  , WB_PC4, REN_1, MEN_0, M_X  , MT_X, ],   
    JAL    : [ Y, BR_J  , OP1_RS1, OP2_IMJ, OEN_0, OEN_0, ALU_X    , WB_PC4, REN_1, MEN_0, M_X  , MT_X, ],

    BEQ    : [ Y, BR_EQ , OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SEQ  , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    BNE    : [ Y, BR_NE , OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SEQ  , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    BLT    : [ Y, BR_LT , OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SLT  , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    BGE    : [ Y, BR_GE , OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SLT  , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    BLTU   : [ Y, BR_LTU, OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SLTU , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],

    BGEU   : [ Y, BR_GEU, OP1_RS1, OP2_IMB, OEN_1, OEN_1, ALU_SLTU , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    ECALL  : [ Y, BR_N  , OP1_X  , OP2_X  , OEN_0, OEN_0, ALU_X    , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
    EBREAK : [ Y, BR_N  , OP1_X  , OP2_X  , OEN_0, OEN_0, ALU_X    , WB_X  , REN_0, MEN_0, M_X  , MT_X, ],
}


#--------------------------------------------------------------------------
#   Control: Control logic (executed in ID stage)
#--------------------------------------------------------------------------

class Control(object):

    def __init__(self):
        super().__init__()

        # Internal signals:----------------------------
        #
        #   self.pc_sel             # Pipe.CTL.pc_sel
        #   self.br_type            # Pipe.CTL.br_type
        #   self.op1_sel            # Pipe.CTL.op1_sel
        #   self.op2_sel            # Pipe.CTL.op2_sel
        #   self.alu_fun            # Pipe.CTL.alu_fun
        #   self.wb_sel             # Pipe.CTL.wb_sel
        #   self.rf_wen             # Pipe.CTL.rf_wen
        #   self.fwd_op1            # Pipe.CTL.fwd_op1
        #   self.fwd_op2            # Pipe.CTL.fwd_op2
        #   self.imem_en            # Pipe.CTL.imem_en
        #   self.imem_rw            # Pipe.CTL.imem_rw
        #   self.dmem_en            # Pipe.CTL.dmem_en
        #   self.dmem_rw            # Pipe.CTL.dmem_rw
        #   self.IF_stall           # Pipe.CTL.IF_stall
        #   self.ID_stall           # Pipe.CTL.ID_stall
        #   self.ID_bubble          # Pipe.CTL.ID_bubble
        #   self.EX_bubble          # Pipe.CTL.EX_bubble
        #   self.MM_bubble          # Pipe.CTL.MM_bubble
        #
        #----------------------------------------------


        # These signals are used before gen() is called
        self.imem_en        = True
        self.imem_rw        = M_XRD


    def gen(self, inst):
        from datapath import Pipe, EX, MM, WB

        opcode = RISCV.opcode(inst)
        if opcode in [ EBREAK, ECALL ]:
            Pipe.ID.exception |= EXC_EBREAK
        elif opcode == ILLEGAL:
            Pipe.ID.exception |= EXC_ILLEGAL_INST
            inst = BUBBLE
            opcode = RISCV.opcode(inst)

        self.IF_stall       = False
        self.ID_stall       = False
        self.ID_bubble      = False
        self.EX_bubble      = False
        self.MM_bubble      = False     

        cs = csignals[opcode]

        self.br_type        = cs[CS_BR_TYPE]
        self.op1_sel        = cs[CS_OP1_SEL]
        self.op2_sel        = cs[CS_OP2_SEL]
        self.alu_fun        = cs[CS_ALU_FUN]
        self.wb_sel         = cs[CS_WB_SEL]
        self.rf_wen         = cs[CS_RF_WEN]

        rs1_oen             = cs[CS_RS1_OEN]
        rs2_oen             = cs[CS_RS2_OEN]

        self.dmem_en        = cs[CS_MEM_EN]
        self.dmem_rw        = cs[CS_MEM_FCN]

        # Control signal to select the next PC
        self.pc_sel         =   PC_BRJMP    if (EX.reg_c_br_type == BR_NE  and (not Pipe.EX.alu_out)) or    \
                                               (EX.reg_c_br_type == BR_EQ  and Pipe.EX.alu_out) or          \
                                               (EX.reg_c_br_type == BR_GE  and (not Pipe.EX.alu_out)) or    \
                                               (EX.reg_c_br_type == BR_GEU and (not Pipe.EX.alu_out)) or    \
                                               (EX.reg_c_br_type == BR_LT  and Pipe.EX.alu_out) or          \
                                               (EX.reg_c_br_type == BR_LTU and Pipe.EX.alu_out) or          \
                                               (EX.reg_c_br_type == BR_J) else                              \
                                PC_JALR     if  EX.reg_c_br_type == BR_JR else                              \
                                PC_4

        # Control signal for forwarding rs1 value to op1_data
        # The c_rf_wen signal can be disabled when we have an exception during dmem access,
        # so Pipe.MM.c_rf_wen should be used instead of MM.reg_c_rf_wen.
        self.fwd_op1        =   FWD_EX      if (EX.reg_rd == Pipe.ID.rs1) and rs1_oen and   \
                                               (EX.reg_rd != 0) and EX.reg_c_rf_wen else    \
                                FWD_MM      if (MM.reg_rd == Pipe.ID.rs1) and rs1_oen and   \
                                               (MM.reg_rd != 0) and Pipe.MM.c_rf_wen else   \
                                FWD_WB      if (WB.reg_rd == Pipe.ID.rs1) and rs1_oen and   \
                                               (WB.reg_rd != 0) and WB.reg_c_rf_wen else    \
                                FWD_NONE

        # Control signal for forwarding rs2 value to op2_data
        self.fwd_op2        =   FWD_EX      if (EX.reg_rd == Pipe.ID.rs2) and               \
                                               (EX.reg_rd != 0) and EX.reg_c_rf_wen and     \
                                               self.op2_sel == OP2_RS2 else                 \
                                FWD_MM      if (MM.reg_rd == Pipe.ID.rs2) and               \
                                               (MM.reg_rd != 0) and Pipe.MM.c_rf_wen and    \
                                               self.op2_sel == OP2_RS2 else                 \
                                FWD_WB      if (WB.reg_rd == Pipe.ID.rs2) and               \
                                               (WB.reg_rd != 0) and WB.reg_c_rf_wen and     \
                                               self.op2_sel == OP2_RS2 else                 \
                                FWD_NONE

        # Control signal for forwarding rs2 value to rs2_data
        self.fwd_rs2        =   FWD_EX      if (EX.reg_rd == Pipe.ID.rs2) and rs2_oen and   \
                                               (EX.reg_rd != 0) and EX.reg_c_rf_wen  else   \
                                FWD_MM      if (MM.reg_rd == Pipe.ID.rs2) and rs2_oen and   \
                                               (MM.reg_rd != 0) and Pipe.MM.c_rf_wen else   \
                                FWD_WB      if (WB.reg_rd == Pipe.ID.rs2) and rs2_oen and   \
                                               (WB.reg_rd != 0) and WB.reg_c_rf_wen  else   \
                                FWD_NONE

        # Check for load-use data hazard
        EX_load_inst = EX.reg_c_dmem_en and EX.reg_c_dmem_rw == M_XRD
        load_use_hazard     = (EX_load_inst and EX.reg_rd != 0) and             \
                              ((EX.reg_rd == Pipe.ID.rs1 and rs1_oen) or        \
                               (EX.reg_rd == Pipe.ID.rs2 and rs2_oen))

        # Check for mispredicted branch/jump
        EX_brjmp            = self.pc_sel != PC_4

        # For load-use hazard, ID and IF are stalled for one cycle (and EX bubbled)
        # For mispredicted branches, instructions in ID and IF should be cancelled (become BUBBLE)
        self.IF_stall       = load_use_hazard 
        self.ID_stall       = load_use_hazard
        self.ID_bubble      = EX_brjmp 
        self.EX_bubble      = load_use_hazard or EX_brjmp

        # Any instruction with an exception becomes BUBBLE as it enters the MM stage. 
        # This is because the instruction can be cancelled while it is in IF and ID due to mispredicted 
        # branch/jump, in which case it should not cause any exception. We just keep track of the exception 
        # state with the instruction along the pipeline until EX. If the instruction survives EX, it is 
        # safe to make the instruction and any following instructions bubble (except for EBREAK)
        self.MM_bubble = (Pipe.EX.exception and (Pipe.EX.exception != EXC_EBREAK)) or (Pipe.MM.exception)
       
        if inst == BUBBLE:
            return False
        else:
            return True
