#==========================================================================
#
#   The PyRISC Project
#
#   sum100.s: Calculates the sum of integers from 1 to 100
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


# This program computes the sum of integers from 1 to 100.
# The x31 register should have the value of 5050 (= 0x13ba) at the end.

    .text
    .align  2
    .globl  _start
_start:                         # code entry point
    li      t0, 1
    li      t1, 100
    li      x31, 0
Loop:
    add     x31, x31, t0
    addi    t0, t0, 1
    ble     t0, t1, Loop
    ebreak

