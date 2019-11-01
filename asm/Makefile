#==========================================================================
#
#   The PyRISC Project
#
#   Makefile
#
#   Jin-Soo Kim
#   Systems Software and Architecture Laboratory
#   Seoul National University
#   http://csl.snu.ac.kr
#
#==========================================================================

PREFIX      = riscv32-unknown-elf-
CC	        = $(PREFIX)gcc
CXX	        = $(PREFIX)g++
AS	        = $(PREFIX)as
OBJDUMP	    = $(PREFIX)objdump

PYRISC      = ../sim/snurisc.py
PYRISCOPT   = -l 1

INCDIR      = 
LIBDIR      =
LIBS        =

CFLAGS      = -Og -march=rv32i -mabi=ilp32 -static 
ASLFAGS     = -march=rv32i -mabi=ilp32 -static 
LDFLAGS     = -T./link.ld -nostdlib -nostartfiles
OBJDFLAGS   = -D --section=.text --section=.data

TARGET      = fib
ASRCS       = fib.s
OBJS        = $(ASRCS:.s=.o)

all: $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $(OBJS) $(LIBDIR) $(LIBS)

.s.o:
	$(CC) -c $(CFLAGS) $(INCDIR) $< -o $@

.c.s:
	$(CC) $(CFLAGS) $(INCDIR) -S $< -o $@

objdump: $(TARGET)
	$(OBJDUMP) $(OBJDFLAGS) $(TARGET) > $(TARGET).objdump    

run: $(TARGET)
	$(PYRISC) $(PYRISCOPT) $(TARGET)

clean:
	$(RM) -f $(TARGET) $(TARGET).objdump $(OBJS) *~ a.out



