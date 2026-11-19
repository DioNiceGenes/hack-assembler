class Parser:
    def __init__(self, input_file):
        self.lines = self._read_input(input_file)
        self.cursor = -1

    def reset_cursor(self) -> None:
        self.cursor = -1

    def _read_input(self, input_file: str) -> list[str]:
        lines = []
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                cleaned_line = self._clean_line(line)
                lines.append(cleaned_line)
        return lines

    def _clean_line(self, line) -> str:
        code = line.partition("//")[0]
        return "".join(code.split())

    def has_more_commands(self) -> bool:
        return self.cursor + 1 < len(self.lines)

    def advance(self) -> None:
        if not self.has_more_commands():
            print("Error: cursor already at the end")
            return
        self.cursor += 1

    def command_type(self) -> str:
        if not (0 <= self.cursor < len(self.lines)):
            raise KeyError(f"Invalid cursor: {self.cursor} when {len(self.lines)} lines")

        if self.lines[self.cursor].startswith("@"):
            return "A"

        if self.lines[self.cursor].startswith("("):
            return "S" #denotes a label

        return "C"

    def symbol(self) -> str:
        cmd_type: str | None = self.command_type()
        if cmd_type not in ("A", "S"):
            raise TypeError("C-instruction can't have a symbol")

        cmd : str = self.lines[self.cursor]
        if cmd_type == "A":
            return cmd[1:]

        return cmd[1:-1]

    def dest(self) -> str:
        if self.command_type() != "C":
            raise ValueError(f"Not a c-instruction: {self.lines[self.cursor]}")

        cmd: str = self.lines[self.cursor]

        if "=" not in cmd:
            return ""

        right: int = cmd.index("=")

        return cmd[:right]

    def comp(self) -> str:
        if self.command_type() != "C":
            raise ValueError(f"Not a c-instruction: {self.lines[self.cursor]}")

        cmd: str = self.lines[self.cursor]

        left: int = cmd.index("=") + 1 if "=" in cmd else 0

        if ";" not in cmd: # no jump part in c-instruction
            return cmd[left:]

        right: int = cmd.index(";")

        return cmd[left:right]

    def jump(self) -> str:
        if self.command_type() != "C":
            raise ValueError(f"Not a c instruction at {self.lines[self.cursor]}")

        cmd: str = self.lines[self.cursor]

        if ";" not in cmd: # no jump part in c-instruction
            return ""

        left: int = cmd.index(";") + 1
        return cmd[left:]
