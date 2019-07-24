"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ST = 0b10000100
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.register[7] = 0xF4
        self.sp = self.register[7]
        self.pc = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ST] = self.handle_ST
        self.branchtable[JMP] = self.handle_JMP

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""
        instructions = []
        if program == "default":
            instructions = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            ]
        else:
            with open(program) as f:
                for line in f:
                    if line[0] == "1" or line[0] == "0":
                        binaryString = line[0:8]
                        binary = int(binaryString, 2)
                        instructions.append(binary)

        address = 0

        for instruction in instructions:
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

    def handle_LDI(self, operand_a, operand_b, operands):
        register = operand_a
        integer = operand_b
        self.register[register] = integer
        self.pc += operands

    def handle_PRN(self, operand_a, operand_b, operands):
        register = operand_a
        print(self.register[register])
        self.pc += operands

    def handle_ADD(self, operand_a, operand_b, operands):
        num1 = self.register[operand_a]
        num2 = self.register[operand_b]
        self.register[operand_a] = num1 + num2
        self.pc += operands
    
    def handle_MUL(self, operand_a, operand_b, operands):
        num1 = self.register[operand_a]
        num2 = self.register[operand_b]
        self.register[operand_a] = num1 * num2
        self.pc += operands

    def handle_PUSH(self, operand_a, operand_b, operands):
        value = self.register[operand_a]
        self.sp -= 1
        self.ram[self.sp] = value
        self.pc += operands
    
    def handle_POP(self, operand_a, operand_b, operands):
        value = self.ram[self.sp]
        self.register[operand_a] = value
        self.sp += 1
        self.pc += operands

    def handle_CALL(self, operand_a, operand_b, operands):
        next_instruction = self.pc + operands
        self.ram[self.sp] = next_instruction
        self.pc = self.register[operand_a]

    def handle_RET(self, operand_a, operand_b, operands):
        next_instruction = self.ram[self.sp]
        self.pc = next_instruction

    def handle_ST(self, operand_a, operand_b, operands):
        address = self.register[operand_a]
        value = self.register[operand_b]
        self.ram[address] = value
        self.pc += operands

    def handle_JMP(self, operand_a, operand_b, operands):
        address = self.register[operand_a]
        self.pc = address

    def run(self):
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if IR in self.branchtable:
                operands = (IR >> 6) + 1
                self.branchtable[IR](operand_a, operand_b, operands)
            elif IR == HLT:
                running = False
            else:
                print("Unfamiliar instruction", '{:b}'.format(IR))
                running = False