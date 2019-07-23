"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        if program == "default":
            program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            ]
        else:
            program_file = open(program)
            instructions = program_file.read()
            program_file.close()
            program = []
            i = 0
            length = len(instructions)
            while i<length:
                current = instructions[i]
                if current == "1" or current == "0":
                    next_num = instructions[i+1]
                    if next_num == "1" or next_num == "0":
                        string = instructions[i:i+8]
                        string = ''.join(string)
                        program.append(int(string, 2))
                        i += 8
                    else:
                        i += 1
                else:
                    i += 1


        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def handle_LDI(self, operand_a, operand_b):
        register = operand_a
        integer = operand_b
        self.register[register] = integer
        self.pc += 3

    def handle_PRN(self, operand_a, operand_b):
        register = operand_a
        print(self.register[register])
        self.pc += 2

    def handle_MUL(self, operand_a, operand_b):
        num1 = self.register[operand_a]
        num2 = self.register[operand_b]
        self.register[operand_a] = num1 * num2
        self.pc += 3

    def run(self):
        running = True
        while running:
            IR = self.pc
            operand = self.ram_read(IR)
            operand_a = self.ram_read(IR+1)
            operand_b = self.ram_read(IR+2)
            if operand in self.branchtable:
                self.branchtable[operand](operand_a, operand_b)
            elif operand == HLT:
                running = False
            else:
                print("Unfamiliar instruction")
                running = False