"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('usage: comp.py + filename')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        # print('her ', line)
                        line = line.split('#', 1)[0]
                        # print('her ', line)
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f'Couldnt find file {sys.argv[1]}')
            sys.exit(1)

        for instruction in self.reg:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        self.load()
        running = True
        SP = 7
      #   CALL = 7
      #   RET = 8

        ops = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100010:  "MUL",
            0b01000101: "PUSH",
            0b01000110: 'POP',
            0b01010000: 'CALL',
            0b00010001: 'RET',
            0b10100000: 'ADD'
        }

        while running:

            inst = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if inst not in ops:
                print(f'Unknown instruction {bin(inst)}')
                break

            elif ops[inst] == 'LDI':
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_num] = value

                self.pc += 3

            elif ops[inst] == 'PRN':
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])

                self.pc += 2

            elif ops[inst] == 'MUL':
                self.reg[operand_a] *= self.reg[operand_b]

                self.pc += 3

            elif ops[inst] == 'PUSH':
                self.reg[SP] -= 1

                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                address_to_push = self.reg[SP]
                self.ram[address_to_push] = value

                self.pc += 2

            elif ops[inst] == 'POP':
                address_to_pop = self.reg[SP]
                value = self.ram[address_to_pop]

                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value

                self.reg[SP] += 1

                self.pc += 2

            elif ops[inst] == 'CALL':
                return_addr = self.pc + 2

                self.reg[SP] -= 1
                address_to_push = self.reg[SP]
                self.ram[address_to_push] = return_addr

                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]

                self.pc = subroutine_addr

            elif ops[inst] == 'RET':
                address_to_pop = self.reg[SP]
                return_addr = self.ram[address_to_pop]
                self.reg[SP] += 1

                self.pc = return_addr

            elif ops[inst] == 'ADD':
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            elif ops[inst] == 'HLT':
                running = False
      #   self.alu(ops, reg_a, reg_b)
