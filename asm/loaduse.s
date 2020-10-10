#==========================================================================
#
#   The PyRISC Project
#
#   loaduse.s: An example of load-use hazard
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


# The following program has a load-use hazard.
# After completing the execution, the x31 register should have the 
# value of 1.

    .text
    .align  2
    .globl  _start
_start:                         # code entry point
    lui     t0, 0x80010
    li      x31, 3
    sw      x31, 0(t0)
    addi    x31, x31, 10
    lw      x31, 0(t0)
    addi    x31, x31, -1
    addi    x31, x31, -1
    ebreak
    


