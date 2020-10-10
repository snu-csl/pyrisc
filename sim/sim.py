#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC: A RISC-V ISA Simulator
#
#   Class for instruction-level simulation.
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
from components import *
from program import *


#--------------------------------------------------------------------------
#   Sim: simulates the CPU execution
#--------------------------------------------------------------------------

class Sim(object):

    @staticmethod
    def run(cpu, entry_point):

        Sim.cpu = cpu
        Sim.cpu.pc.write(entry_point)

        while True:
            # Execute a single instruction
            status = Sim.single_step()

            # Update stats
            Stat.cycle      += 1
            Stat.icount     += 1

            # Show logs after executing a single instruction
            if Log.level >= 5:
                Sim.cpu.regs.dump()
            if Log.level >= 6:
                Sim.cpu.dmem.dump(skipzero = True)

            if not status == EXC_NONE:
                break;
      
        # Handle exceptions, if any
        if (status & EXC_DMEM_ERROR):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_DMEM_ERROR], Sim.cpu.pc.read()))
        elif (status & EXC_EBREAK):
            print("Execution completed")
        elif (status & EXC_ILLEGAL_INST):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_ILLEGAL_INST], Sim.cpu.pc.read()))
        elif (status & EXC_IMEM_ERROR):
            print("Exception '%s' occurred at 0x%08x -- Program terminated" % (EXC_MSG[EXC_IMEM_ERROR], Sim.cpu.pc.read()))

        # Show logs after finishing the program execution
        if Log.level > 0:
            if Log.level < 5:
                Sim.cpu.regs.dump()
            if Log.level > 1 and Log.level < 6:
                Sim.cpu.dmem.dump(skipzero = True)

    @staticmethod
    def log(pc, inst, rd, wbdata, pc_next):

        if Stat.cycle < Log.start_cycle:
            return
        if Log.level >= 4:
            info = "# R[%d] <- 0x%08x, pc_next=0x%08x" % (rd, wbdata, pc_next) if rd else \
                   "# pc_next=0x%08x" % pc_next
        else:
            info = ''
        if Log.level >= 3:
            print("%d 0x%08x: %-30s%-s" % (Stat.cycle, pc, Program.disasm(pc, inst), info))
        else:
            return

    def run_alu(pc, inst, opcode, cs):
        np.seterr(all='ignore')

        Stat.inst_alu += 1

        rs1         = RISCV.rs1(inst)
        rs2         = RISCV.rs2(inst)
        rd          = RISCV.rd(inst)

        imm_i       = RISCV.imm_i(inst)
        imm_u       = RISCV.imm_u(inst)

        rs1_data    = Sim.cpu.regs.read(rs1)
        rs2_data    = Sim.cpu.regs.read(rs2)

        alu1        = rs1_data      if cs[IN_ALU1] == OP1_RS1    else \
                      pc            if cs[IN_ALU1] == OP1_PC     else \
                      WORD(0)       

        alu2        = rs2_data      if cs[IN_ALU2] == OP2_RS2    else \
                      imm_i         if cs[IN_ALU2] == OP2_IMI    else \
                      imm_u         if cs[IN_ALU2] == OP2_IMU    else \
                      WORD(0)

        
        alu_out     = WORD(alu1 + alu2)                     if (cs[IN_OP] == ALU_ADD)           else \
                      WORD(alu1 - alu2)                     if (cs[IN_OP] == ALU_SUB)           else \
                      WORD(alu1 & alu2)                     if (cs[IN_OP] == ALU_AND)           else \
                      WORD(alu1 | alu2)                     if (cs[IN_OP] == ALU_OR)            else \
                      WORD(alu1 ^ alu2)                     if (cs[IN_OP] == ALU_XOR)           else \
                      WORD(1)                               if (cs[IN_OP] == ALU_SLT and             \
                                                                (SWORD(alu1) < SWORD(alu2)))    else \
                      WORD(1)                               if (cs[IN_OP] == ALU_SLTU and            \
                                                                (alu1 < alu2))                  else \
                      WORD(alu1 << (alu2 & 0x1f))           if (cs[IN_OP] == ALU_SLL)           else \
                      WORD(SWORD(alu1) >> (alu2 & 0x1f))    if (cs[IN_OP] == ALU_SRA)           else \
                      WORD(alu1 >> (alu2 & 0x1f))           if (cs[IN_OP] == ALU_SRL)           else \
                      WORD(0)

        pc_next     = pc + 4

        Sim.cpu.regs.write(rd, alu_out)
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, alu_out, pc_next)
        return EXC_NONE

    def run_mem(pc, inst, opcode, cs):

        Stat.inst_mem += 1
       
        rs1         = RISCV.rs1(inst)
        rs1_data    = Sim.cpu.regs.read(rs1)

        if (cs[IN_OP] == MEM_LD):
            rd          = RISCV.rd(inst)
            imm_i       = RISCV.imm_i(inst)
            mem_addr    = rs1_data + SWORD(imm_i)
            mem_data, dmem_ok = Sim.cpu.dmem.access(True, mem_addr, 0, M_XRD)
            if dmem_ok:
                Sim.cpu.regs.write(rd, mem_data)
        else:
            rd          = 0                     
            rs2         = RISCV.rs2(inst)
            rs2_data    = Sim.cpu.regs.read(rs2)

            imm_s       = RISCV.imm_s(inst)
            mem_addr    = rs1_data + SWORD(imm_s)
            mem_data, dmem_ok = Sim.cpu.dmem.access(True, mem_addr, rs2_data, M_XWR)

        if not dmem_ok:
            return EXC_DMEM_ERROR

        pc_next         = pc + 4
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, mem_data, pc_next)
        return EXC_NONE

    def run_ctrl(pc, inst, opcode, cs):

        Stat.inst_ctrl += 1

        if inst in [ EBREAK, ECALL ]:
            Sim.log(pc, inst, 0, 0, 0) 
            return EXC_EBREAK

        rs1             = RISCV.rs1(inst)
        rs2             = RISCV.rs2(inst)
        rd              = RISCV.rd(inst)
        rs1_data        = Sim.cpu.regs.read(rs1)
        rs2_data        = Sim.cpu.regs.read(rs2)

        imm_i           = RISCV.imm_i(inst)
        imm_j           = RISCV.imm_j(inst)
        imm_b           = RISCV.imm_b(inst)
        pc_plus4        = pc + 4

        pc_next         = pc + imm_j        if opcode == JAL    else                                             \
                          pc + imm_b        if (opcode == BEQ and rs1_data == rs2_data) or                       \
                                                (opcode == BNE and not (rs1_data == rs2_data)) or                \
                                                (opcode == BLT and SWORD(rs1_data) < SWORD(rs2_data)) or         \
                                                (opcode == BGE and not (SWORD(rs1_data) < SWORD(rs2_data))) or   \
                                                (opcode == BLTU and WORD(rs1_data) < WORD(rs2_data)) or          \
                                                (opcode == BGEU and not (WORD(rs1_data) < WORD(rs2_data)))  else \
                          (rs1_data + imm_i) & WORD(0xfffffffe)     if opcode == JALR   else                     \
                          pc_plus4

        if (opcode in [ JAL, JALR ]):
            Sim.cpu.regs.write(rd, pc_plus4)
        Sim.cpu.pc.write(pc_next)
        Sim.log(pc, inst, rd, pc_plus4, pc_next) 
        return EXC_NONE


    func = [ run_alu, run_mem, run_ctrl ]

    @staticmethod
    def single_step():

        pc      = Sim.cpu.pc.read()

        # Instruction fetch
        inst, imem_status = Sim.cpu.imem.access(True, pc, 0, M_XRD)
        if not imem_status:
            return EXC_IMEM_ERROR

        # Instruction decode 
        opcode  = RISCV.opcode(inst)
        if opcode == ILLEGAL:
            return EXC_ILLEGAL_INST

        cs = isa[opcode]
        return Sim.func[cs[IN_CLASS]](pc, inst, opcode, cs)

