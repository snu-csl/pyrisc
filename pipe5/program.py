#==========================================================================
#
#   The PyRISC Project
#
#   SNURISC5: A 5-stage Pipelined RISC-V ISA Simulator
#
#   Classes for program loading, disassembling, logging, and run-time stats.
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================

from elftools.elf import elffile as elf
from consts import *
from isa import *
from components import *


#--------------------------------------------------------------------------
#   AsmCache: temporarily caches disassembled instructions
#--------------------------------------------------------------------------

class AsmCache(object):
    def __init__(self):
        self.cache = { }

    def add(self, pc, asm):
        self.cache[pc] = asm

    def lookup(self, pc):
        # returns None if not found
        return self.cache.get(pc)


#--------------------------------------------------------------------------
#   Program: loads an ELF file into memory and supports disassembling
#--------------------------------------------------------------------------

ELF_OK              = 0
ELF_ERR_OPEN        = 1
ELF_ERR_CLASS       = 2
ELF_ERR_DATA        = 3
ELF_ERR_TYPE        = 4
ELF_ERR_MACH        = 5

ELF_ERR_MSG = {
    ELF_ERR_OPEN    : 'File %s not found',
    ELF_ERR_CLASS   : 'File %s is not a 32-bit ELF file',
    ELF_ERR_DATA    : 'File %s is not a little-endian ELF file',
    ELF_ERR_TYPE    : 'File %s is not an executable file',
    ELF_ERR_MACH    : 'File %s is not an RISC-V executable file',
}

class Program(object):


    def __init__(self):
        Program.asmcache = AsmCache()


    def check_elf(self, filename, header):
        e_ident = header['e_ident']

        # This is already checked during ELFFile() 
        '''
        if bytes(e_ident['EI_MAG']) != b'\x7fELF':
            print("File %s is not an ELF file" % filename)
            return False
        '''

        if e_ident['EI_CLASS'] != 'ELFCLASS32':
            return ELF_ERR_CLASS
        if e_ident['EI_DATA'] != 'ELFDATA2LSB':
            return ELF_ERR_DATA
        if header['e_type'] != 'ET_EXEC':
            return ELF_ERR_TYPE
        # Old elftools do not recognize EM_RISCV
        if header['e_machine'] != 'EM_RISCV' and header['e_machine'] != 243:
            return ELF_ERR_MACH
        return ELF_OK


    def load(self, cpu, filename):
        print("Loading file %s" % filename)
        try:
            f = open(filename, 'rb')
        except IOError:
            print(ELF_ERR_MSG[ELF_ERR_OPEN] % filename) 
            return WORD(0)

        with f:
            ef = elf.ELFFile(f)
            efh = ef.header
            ret = self.check_elf(filename, efh)
            if ret != ELF_OK:
                print(ELF_ERR_MSG[ret] % filename)
                return WORD(0)

            entry_point = WORD(efh['e_entry'])
            
            for seg in ef.iter_segments():
                addr = seg.header['p_vaddr']
                memsz = seg.header['p_memsz']
                if seg.header['p_type'] != 'PT_LOAD':
                    continue
                if addr >= cpu.imem.mem_start and addr + memsz < cpu.imem.mem_end:
                    mem = cpu.imem
                elif addr >= cpu.dmem.mem_start and addr + memsz < cpu.dmem.mem_end:
                    mem = cpu.dmem
                else:
                    print("Invalid address range: 0x%08x - 0x%08x" \
                        % (addr, addr + memsz - 1))
                    continue
                image = seg.data()
                for i in range(0, len(image), WORD_SIZE):
                    c = int.from_bytes(image[i:i+WORD_SIZE], byteorder='little')
                    mem.access(True, addr, c, M_XWR)
                    addr += WORD_SIZE
            return entry_point
                   
    @staticmethod
    def disasm(pc, inst):

        if inst == BUBBLE:
            asm = "BUBBLE"
            return asm
        elif inst == NOP:
            asm = "nop"
            return asm

        asm = Program.asmcache.lookup(pc)
        if asm is not None:
            return asm

        opcode = RISCV.opcode(inst)
        if opcode == ILLEGAL:
            asm = "(illegal)"
            Program.asmcache.add(pc, asm)
            return asm

        info    = isa[opcode]
        opname  = RISCV.opcode_name(opcode)
        rs1     = RISCV.rs1(inst)
        rs2     = RISCV.rs2(inst)
        rd      = RISCV.rd(inst)
        imm_i   = RISCV.imm_i(inst)
        imm_s   = RISCV.imm_s(inst)
        imm_b   = RISCV.imm_b(inst)
        imm_u   = RISCV.imm_u(inst)
        imm_j   = RISCV.imm_j(inst)
        if info[IN_TYPE] == R_TYPE:
            asm = "%-7s%s, %s, %s" % (opname, rname[rd], rname[rs1], rname[rs2])
        elif info[IN_TYPE] == I_TYPE:
            asm = "%-7s%s, %s, %d" % (opname, rname[rd], rname[rs1], SWORD(imm_i))
        elif info[IN_TYPE] == IL_TYPE:
            asm = "%-7s%s, %d(%s)" % (opname, rname[rd], SWORD(imm_i), rname[rs1])
        elif info[IN_TYPE] == IJ_TYPE:
            asm = "%-7s%s, %s, %d" % (opname, rname[rd], rname[rs1], SWORD(imm_i))
        elif info[IN_TYPE] == IS_TYPE:
            asm = "%-7s%s, %s, %d" % (opname, rname[rd], rname[rs1], SWORD(imm_i & 0x1f))
        elif info[IN_TYPE] == U_TYPE:
            asm = "%-7s%s, 0x%05x" % (opname, rname[rd], imm_u)
        elif info[IN_TYPE] == S_TYPE:
            asm = "%-7s%s, %d(%s)" % (opname, rname[rs2], SWORD(imm_s), rname[rs1])
        elif info[IN_TYPE] == B_TYPE:
            asm = "%-7s%s, %s, 0x%08x" % (opname, rname[rs1], rname[rs2], pc + SWORD(imm_b))
        elif info[IN_TYPE] == J_TYPE:
            asm = "%-7s%s, 0x%08x" % (opname, rname[rd], pc + SWORD(imm_j))
        elif info[IN_TYPE] == X_TYPE:
            return info[IN_NAME]
        else:
            asm = "(unknown)"

        Program.asmcache.add(pc, asm)
        return asm


#--------------------------------------------------------------------------
#   Log: supports logging
#--------------------------------------------------------------------------

class Log(object):

    MAX_LOG_LEVEL   = 7         # last log level

    level           = 4         # default log level
    start_cycle     = 0


#--------------------------------------------------------------------------
#   Stat: supports run-time stat collecting and printing
#--------------------------------------------------------------------------

class Stat(object):

    cycle           = 0         # number of CPU cycles
    icount          = 0         # number of instructions executed

    inst_alu        = 0         # number of ALU instructions
    inst_mem        = 0         # number of load/store instructions
    inst_ctrl       = 0         # number of control transfer instructions

    @staticmethod
    def show():
        print("%d instructions executed in %d cycles. CPI = %.3f" % (Stat.icount, Stat.cycle, 0.0 if Stat.icount == 0 else  Stat.cycle / Stat.icount))
        print("Data transfer:    %d instructions (%.2f%%)" % (Stat.inst_mem, 0.0 if Stat.icount == 0 else Stat.inst_mem * 100.0 / Stat.icount))
        print("ALU operation:    %d instructions (%.2f%%)" % (Stat.inst_alu, 0.0 if Stat.icount == 0 else Stat.inst_alu * 100.0 / Stat.icount))
        print("Control transfer: %d instructions (%.2f%%)" % (Stat.inst_ctrl, 0.0 if Stat.icount == 0 else Stat.inst_ctrl * 100.0 / Stat.icount))


