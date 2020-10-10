#==========================================================================
#
#   The PyRISC Project
#
#   branch.s: An example of mispredicted branch
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


# The following program has a mispredicted branch instruction.
# After completing the execution, the x31 register should have the 
# value of 12 (= 0x0c).

    .text
    .align  2
    .globl  _start
_start:                         # code entry point
    li      t0, 1
    li      t1, 2
    li      x31, 0
    bne     t0, t1, Exit
    addi    x31, x31, 1
    addi    x31, x31, 2
Exit:
    addi    x31, x31, 4
    addi    x31, x31, 8
    ebreak
    


