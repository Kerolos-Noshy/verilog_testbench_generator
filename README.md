# Verilog testbench generator
## Overview
This project is a Python script that generates a Verilog testbench file using the HDLVerilog library. The generated testbench can be used to simulate the behavior of a digital logic design described in Verilog.

## Installation
To use this script, you will need to have Python and the HDLVerilog library installed on your system.

## Prerequisites
- Python 3.x
- HDLVerilog library
- You can install the dependencies by running the following command:
  - `pip install hdldesign`


## Important Note
 - This script doesn't generate a correct testbench if the verilog code has `clk` or `rst` (_may be we implement it soon_)
