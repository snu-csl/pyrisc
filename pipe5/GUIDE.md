# The PyRISC Project
# SNURISC5: A 5-Stage Pipelined RISC-V Simulator
# Development Guide

## Introduction

This file describes the internal architecture and implementation details of the `snurisc5` 5-stage pipelined RISC-V simulator. Please read this file carefully if you want to modify the simulator.

## Overall simulator architecture

### Program structure

The `snurisc5` simulator consists of the following files written in Python.

* `snurisc5.py`: This is the main file that accepts and parses arguments from the user. Also, the `main()` function in this file controls the overall simulation.
* `program.py`: The main function of this file is to load the contents of the input RISC-V executable file to the instruction memory (`load()`). It also provides the `disasm()` function that is used to disassemble the given 32-bit binary instruction word to the corresponding assembly code in a textual form. The disassembled code is stored in the `AsmCache` using the program counter (`pc`) value as a key to avoid the repeated disassembling for the same instruction.
* `datapath.py`: This file contains the datapath information for each stage.
* `control.py`: This file contains the control logic.
* `components.py`: This file has various hardware components used in the datapath such as `RegisterFile`, `Register`, `Memory`, `ALU`, and `Adder`. Each component is instantiated wherever necessary in the datapath.
* `isa.py`: This file has the definition of each instruction and decoding logic for RV32I RISC-V instruction set.
* `consts.py`: This file defines various constants used throughout the simulator

### Main simulation flow

The execution of the simulator starts from the `main()` function in `snurisc5.py`. The main simulation flow is simple as shown below: (1) It first reads and parses arguments, (2) Makes a CPU instance and a program instance, (3) Loads a program, (4) Runs the program, and (5) Shows various statistics information including CPI.

```
def main():

    filename = parse_args(sys.argv)         # parse arguments
    if not filename:                        # if parse error, exit
        show_usage(sys.argv[0])
        sys.exit()

    cpu = SNURISC5()                        # make a CPU instance with hw components
    prog = Program()                        # make a program instance
    entry_point = prog.load(cpu, filename)  # load a program
    if not entry_point:                     # if no entry point, exit
        sys.exit()
    cpu.run(entry_point)                    # run the program starting from entry_point
    Stat.show()                             # show stats
```


### Simulation loop

The `Pipe` class in the `datapath.py` file controls the actual execution of the program. It obtains the information of each stage during the initialization step `set_stages()`. As you can see below, `Pipe.IF`, `Pipe.ID`, `Pipe.EX`, `Pipe.MM`, and `Pipe.WB` points to the corresponding objects of the `IF`, `ID`, `EX`, `MM`, and `WB` classes, respectively. Also, `Pipe.CTL` points to the object of the `Control` class.
```
    def set_stages(cpu, stages, ctl):
        Pipe.cpu = cpu
        Pipe.stages = stages
        Pipe.IF = stages[S_IF]
        Pipe.ID = stages[S_ID]
        Pipe.EX = stages[S_EX]
        Pipe.MM = stages[S_MM]
        Pipe.WB = stages[S_WB]
        Pipe.CTL = ctl
```

The `run()` method in the `Pipe` class is the actual simulation loop. First, it initializes the `pc` register with the `entry_point` value, and runs over a single cycle at a time until it meets any exception in the WB stage, which is summarized below.
```
    def run(entry_point):
        IF.reg_pc = entry_point
        while True:
            Pipe.WB.compute()
            Pipe.MM.compute()
            Pipe.EX.compute()
            Pipe.ID.compute()
            Pipe.IF.compute()

            Pipe.IF.update()
            Pipe.ID.update()
            Pipe.EX.update()
            Pipe.MM.update()
            ok = Pipe.WB.update()

            if not ok:
                break;
```

Each stage consists of two _phases_, namely, `compute()` and `update()`. For any stage `S`, `S.compute()` represents the manipulation of signals using some combinational logic performed inside of the stage, while `S.update()` indicates the step where the contents of the pipeline registers (between the current and the next stage) are updated. In the real processor, all the `*.compute()` phases are performed in parallel and all the state updates specified in `*.update()` are done at once (e.g., on the rising edge of the clock). However, we just serialize the execution of `*.compute()` and `*.update()` to simplify the simulator.

Note that we run each stage in the reverse order of the pipeline, especially for the `*.compute()` phases. This is because that hazard detection and forwarding detection logic depends on the previous instructions in the pipeline. For example, the forwarding logic in the ID stage depends on the signals in the EX, MM, WB stages, hence EX, MM, WB stages should be run before ID. Similarly, the branch outcome is determined in the EX stage which means that the EX stage should be completed before the IF stage. For these reasons, it is safe to run each stage in the reverse order such as WB -> MM -> EX -> ID -> IF. Because all the internal signals are already generated during `*.compute()` phases, the execution of `*.update()` phases can be done in any order, but we run them sequentially from ID to WB.


## Naming conventions

### Pipeline registers

In `snurisc5`, pipeline registers are implemented as class variables. For each stage, we have a class definition, such as `IF`, `ID`, `EX`, `MM`, or `WB`. For class variables, their values can be referenced directly by prefixing the class name to the variable name. In addition, we always add the prefix `reg_` to the names of pipeline registers to explicitly denote they belong to the pipeline registers. For example, `EX.reg_rd` represents the register named `reg_rd` in the set of pipeline registers between the ID and the EX stages.

### Internal signals within a stage

Internal signals used within a stage are implemented as instance variables in the corresponding object. For example, `self.rd` indicates an internal signal named `rd`. As they are instance variables, the same signal can be freely used either in `compute()` or in `update()`. Also it is possible that two different stages can define their own `self.rd` variables because each stage is represented by a different object. Recall that `Pipe.IF`, `Pipe.ID`, `Pipe.EX`, `Pipe.MM`, and `Pipe.WB` point to each _object_ that corresponds to each stage. Therefore, the `self.rd` defined in the ID stage (i.e., in the `Pipe.ID` object) can be referenced as `Pipe.ID.rd`. Likewise, `Pipe.EX.rd` represents the `self.rd` variable defined in the EX stage (i.e., in the `Pipe.EX` object).

The following highlights the differences between pipeline registers and internal signals.
```
EX.reg_rd      # A pipeline register between ID and EX. Always start with 'reg_'.
Pipe.EX.rd     # An internal signal within EX. Can be referenced as `self.rd` within the EX stage.
```

## Usage conventions

Note that the contents of the pipeline registers are updated at the end of each cycle in `*.update()` functions. Consider the situation where you simply want to pass the `rd` register number from EX to MM stage. You may try this as follows:
```
# In EX.update()

MM.reg_rd = EX.reg_rd               # Wrong example
```

But the problem is that `EX.reg_rd` is also a pipeline register and its value can be updated in `ID.update()` before `MM.reg_rd`. In this case, the previous value of `EX.reg_rd` will be lost. For this reason, it is always safer if you read out the value of `EX.reg_rd` to an internal signal first and use this signal to update the pipeline register, as shown below.
```
# In EX.compute()
self.rd = EX.reg_rd  # Read out the pipeline register to an internal signal

# In EX.update()
MM.reg_rd = self.rd  # Update the pipeline register using the internal signal
```

In the above example, even if the value of `EX.reg_rd` is changed during `ID.update()` before `MM.reg_rd`, the local signal `self.rd` remains the same which makes `MM.reg_rd` receive the correct value.

## Example

Assume that we have an entry called `exception` in the MM pipeline registers that sit between the EX stage and the MM stage. This signal needs to be delivered to the WB stage. However, during the MM stage, this signal can be modified due to any exception in the data memory (dmem) access. The following figure shows this situation.

```
 --- EX stage ---     MM pipeline registers    --- MM stage --     WB pipeline registers
                     +--------------------+                       +--------------------+
                     |         ...        |  +-self.exception     |         ...        |
                     +--------------------+  |    +-------+       +--------------------+
                     |     exception      |  V    |       |       |     exception      |
self.exception  ---->| (MM.reg_exception) |------>|       |------>| (WB.reg_exception) |
                     +--------------------+       |       |       +--------------------+
                     |                    |       +-------+       |                    |
                     +--------------------+           ^           +--------------------+
                     |         ...        |           | status    |                    |
```

The above situation can be implemented as follows:

1. Read out the value of the pipeline register and stores it in the internal signal
```
# In MM.compute()
    self.exception = MM.reg_exception
```
2. Modify the signal according to the status of dmem access
```
# In MM.compute()
    mem_data, status = Pipe.cpu.dmem.access(...)
    if not status:
        self.exception |= EXC_DMEM_ERROR
```
3. Deliver it to the WB pipeline register
```
# In MM.update()
    WB.reg_exception = self.exception
```

---
Jin-Soo Kim<br>
Systems Software and Architecture Laboratory<br>
Seoul National University<br>
http://csl.snu.ac.kr
