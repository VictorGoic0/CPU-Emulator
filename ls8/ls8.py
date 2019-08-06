#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program = "default"
if len(sys.argv) == 2:
    program = sys.argv[1]
elif len(sys.argv) > 2:
    print("Only one program can be ran at a time. First argument will be used.")
    program = sys.argv[1]
elif len(sys.argv) < 2:
    print("No program provided. Default program will be ran.")
cpu.load(program)
cpu.run()