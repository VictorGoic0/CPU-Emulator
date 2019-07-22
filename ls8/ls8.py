#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program = "default"
if 1 in sys.argv:
    program = sys.argv[1]
cpu.load(program)
cpu.run()