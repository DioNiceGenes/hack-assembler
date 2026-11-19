# Hack Assembler

A two-pass assembler written in Python for [Nand2Tetris Project 6](https://www.nand2tetris.org/project06). It translates Hack assembly (`.asm`) into 16-bit Hack machine instructions (`.hack`).

This is a learning project built while completing Part I of *The Elements of Computing Systems*.

## Requirements

- Python 3.10 or newer
- No third-party dependencies

## Usage

Run from the project directory:

```bash
python3 main.py tests/Add.asm
```

This creates `tests/Add.hack`. The output is written beside the input file, replacing the `.asm` extension with `.hack`. Existing output at that path is overwritten.

Paths to other assembly files work too:

```bash
python3 main.py /path/to/Program.asm
```

Each output line contains one 16-bit binary instruction. Comments, blank lines, and label declarations generate no output.

## Supported features

- Numeric A-instructions, with addresses from 0 to 32767
- C-instructions with optional destination and jump fields
- All 28 standard computation mnemonics
- Predefined symbols: `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `R0`–`R15`, `SCREEN`, and `KBD`
- Labels and forward references
- Variables allocated from RAM address 16
- Whitespace and `//` comments, including inline comments

The assembler expects valid Hack assembly. It reports several invalid inputs with Python exceptions; it is not a complete syntax validator.

## Architecture

| Module | Responsibility |
| --- | --- |
| `main.py` | Command-line entry point, two-pass assembly, and output |
| `parser.py` | Input cleaning, instruction classification, and field extraction |
| `code_encoding.py` | Destination, computation, and jump encoding tables |
| `symbol_table.py` | Predefined and user-defined symbol addresses |

The first pass records labels using ROM instruction addresses. The second pass resolves symbols, allocates variables, and writes machine instructions. Labels do not increment the ROM address counter.

## Checking the output

The `tests/` directory contains the course's assembly examples, rather than an automated Python test suite. To translate all of them:

```bash
for source in tests/*.asm; do
    python3 main.py "$source" || break
done
```

Compare each generated `.hack` file with the output of the official assembler for the exact same `.asm` input. The [online assembler](https://nand2tetris.github.io/web-ide/asm/) provides Source, Binary Code, and Compare Code panels.

Suggested order:

1. `Add.asm`
2. `MaxL.asm`, `RectL.asm`, and `PongL.asm` (without symbols)
3. `Max.asm`, `Rect.asm`, and `Pong.asm` (with symbols)

Generated `.hack` files are ignored by Git and can be recreated with the commands above.

## Credits

The Hack architecture, assembler specification, and assembly examples in `tests/` come from the Nand2Tetris course and *The Elements of Computing Systems* by Noam Nisan and Shimon Schocken (MIT Press). Original attribution comments are retained in the example files.

- [Project 6 specification](https://www.nand2tetris.org/project06)
- [Official tools and project materials](https://www.nand2tetris.org/software)

This repository contains a student implementation of the assembler, not an official course solution.
