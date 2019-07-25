"""CPU functionality."""

import sys
import time
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
PRA = 0b01001000
IRET = 0b00010011
CMP = 0b10100111
# INT = 0b01010010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.register[7] = 0xF4
        self.sp = self.register[7]
        self.IS = self.register[6]
        self.im = self.register[5]
        self.pc = 0
        self.fl = 0b00000000
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
        self.branchtable[PRA] = self.handle_PRA
        self.branchtable[IRET] = self.handle_IRET
        self.branchtable[CMP] = self.handle_CMP
        # self.branchtable[INT] = self.handle_INT

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

    def handle_PRA(self, operand_a, operand_b, operands):
        value = self.register[operand_a]
        print(chr(value))
        self.pc += operands

    def handle_IRET(self, operand_a, operand_b, operands):
        for i in range(6, -1, -1):
            self.manual_POP(i)
        self.fl = self.ram[self.sp]
        self.sp += 1
        self.pc = self.ram[self.sp]
        self.sp += 1

    def handle_CMP(self, operand_a, operand_b, operands):
        value_1 = self.register[operand_a]
        value_2 = self.register[operand_b]
        if value_1 > value_2:
            self.fl = 0b00000010
        elif value_1 == value_2:
           self.fl = 0b00000001
        else:
            self.fl = 0b00000100

    # def handle_INT(self, operand_a, operand_b, operands):
    #     interrupt_number = self.register[operand_a]
    #     # Set nth bit in IS register to this value ??
    #     self.IS = self.IS | interrupt_number
    #     self.pc += operands

    def manual_PUSH(self, value):
        self.sp -= 1
        self.ram[self.sp] = value

    def manual_POP(self, operand_a):
        value = self.ram[self.sp]
        self.register[operand_a] = value
        self.sp += 1

    def run(self):
        running = True
        start_time = time.time()
        while running:
            if self.IS == 0b00000001:
                masked_interrupts = self.im & self.IS
                for i in range(8):
                    interrupt = ((masked_interrupts >> i) & 1) == 1
                    if interrupt:
                        self.IS = 0
                        self.manual_PUSH(self.pc)
                        self.manual_PUSH(self.fl)
                        for i in range(7):
                            self.manual_PUSH(self.register[i])
                        handler_address = self.ram[0xF8]
                        self.pc = handler_address
                        break
                    else:
                        continue
            current_time = time.time()
            if current_time >= 1:
                start_time = time.time()
                self.IS = 0b00000001
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