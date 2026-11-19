import sys

from code_encoding import Code
from parser import Parser
from symbol_table import SymbolTable


class Assembler:
    def __init__(self, input_file: str):
        self.parser = Parser(input_file)
        self.encoder = Code()
        self.symbol_table = SymbolTable()
        self.output_name = self._output_name(input_file)

    def _output_name(self, input_file: str) -> str:
        if not input_file.endswith(".asm"):
            raise ValueError(f"Expected an .asm file: {input_file}")

        return input_file[:-4] + ".hack"

    def first_pass(self) -> None:
        self.rom_counter: int = 0

        while self.parser.has_more_commands():
            self.parser.advance()

            if self.parser.command_type() in ("A", "C"): # instruction -> counter++
                self.rom_counter += 1
            else:
                symbol: str = self.parser.symbol()
                self.symbol_table.add_entry(symbol, self.rom_counter)

    def _handle_cinstruction(self) -> str:
        dest_mnemonics: str = self.parser.dest()
        dest_bits: str = self.encoder.dest(dest_mnemonics)

        comp_mnemonic: str = self.parser.comp()
        comp_bits: str = self.encoder.comp(comp_mnemonic)

        jump_mnemonic: str = self.parser.jump()
        jump_bits = self.encoder.jump(jump_mnemonic)

        return "111" + comp_bits + dest_bits + jump_bits

    def _encode(self, num: int) -> str:
        if not (0 <= num <= 32767):
            raise ValueError(f"A-instruction address out of range: {num}")
        return f"{num:016b}"

    def _handle_ainstruction(self) -> str:
        symbol: str = self.parser.symbol()

        # numeric address,
        if symbol.isnumeric():
            return self._encode(int(symbol))

        # unknown symbolic value, we save it
        if not self.symbol_table.contains(symbol):
            self.symbol_table.add_entry(symbol, self.ram_counter)
            self.ram_counter += 1

        addr: int = self.symbol_table.get_address(symbol)
        return self._encode(addr)


    def second_pass(self) -> None:
        self.ram_counter: int = 16
        self.parser.reset_cursor()


        with open(self.output_name, "w", encoding="utf-8") as out_file:
            while self.parser.has_more_commands():
                self.parser.advance()

                cmd_type: str = self.parser.command_type()

                if cmd_type == "C":
                    machine_code = self._handle_cinstruction()
                elif cmd_type == "A":
                    machine_code = self._handle_ainstruction()
                else:
                    continue

                out_file.write(machine_code + '\n')

    def assemble(self):
        self.first_pass()
        self.second_pass()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input.asm>", file=sys.stderr)
        sys.exit(1)

    assembler = Assembler(sys.argv[1])
    assembler.assemble()
