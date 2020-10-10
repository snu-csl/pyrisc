#==========================================================================
#
#   The PyRISC Project
#
#   fib.s: Computes fibonacci numbers recursively
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================


# The following sample code computes the Fibonnaci number given by:
#   fib(n) = fib(n-1) + fib(n-2)        (if n > 1)
#          = 1                          (if n <= 1)
# After completing the execution of this program, the a0 register should
# have the value fib(5) = 8.


    .text
    .align  2
    .globl  _start
_start:                         # code entry point
    lui     sp, 0x80020         # set the stack pointer to 0x80020000
    li      a0, 5               # set the argument
    call    fib                 # call fib(5)
    ebreak                      # terminate the program

fib:
    li      a5, 1               # a5 <- 1
    ble     a0, a5, Exit        # if (n <= 1) goto Exit

    addi    sp, sp, -16         # make a room in the stack  
    sw      ra, 12(sp)          # save ra register
    sw      s0, 8(sp)           # save s0 register
    sw      s1, 4(sp)           # save s1 register

    mv      s0, a0              # s0 <- n
    addi    a0, a0, -1          # a0 <- n - 1
    call    fib                 # call fib(n-1)
    mv      s1, a0              # s1 <- fib(n-1)
    addi    a0, s0, -2          # a0 <- n - 2
    call    fib                 # call fib(n-2)
    add     a0, s1, a0          # a0 = fib(n-1) + fib(n-2)

    lw      ra, 12(sp)          # restore ra
    lw      s0, 8(sp)           # restore s0
    lw      s1, 4(sp)           # restore s1
    addi    sp, sp, 16          # restore the stack pointer
    ret

Exit:
    li      a0, 1               # a0 <- 1
    ret


