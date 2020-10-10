#==========================================================================
#
#   The PyRISC Project
#
#   forward.s: An example of data forwarding
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


# The following program has several situations that require data forwarding.
# After successful completion, the x31 register should have the 
# value of 9.

    .text
    .align  2
    .globl  _start
_start:                         # code entry point
    li      x31, 0
    li      t0, 1
    li      t1, 2
    li      t2, 3
    add     x31, x31, t2
    add     x31, x31, t2
    add     x31, x31, t1
    add     x31, x31, t0
    ebreak


