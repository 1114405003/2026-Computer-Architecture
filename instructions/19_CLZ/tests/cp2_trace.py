"""Trace the RV32I instructions used by the CP2 CLZ baseline.

This is a small executable reference for the instruction-count table. It
supports exactly the instructions used by src/rv32im/clz.s.
"""

from pathlib import Path
import re


ASM = Path(__file__).parents[1] / "src" / "rv32im" / "clz.s"
TESTS = (0x80000000, 0x00010000, 0x00000001, 0x00000000)
EXPECTED = {0x80000000: 0, 0x00010000: 15, 0x00000001: 31, 0x00000000: 32}
REGISTERS = {"zero": 0, "a0": 10, "t0": 5, "t1": 6}
BRANCHES = {"beq", "bnez"}


def load_program():
    instructions = []
    labels = {}
    for raw_line in ASM.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = len(instructions)
            continue
        match = re.match(r"([^:]+):\s*(.*)", line)
        if match:
            labels[match.group(1)] = len(instructions)
            line = match.group(2).strip()
        if line.startswith("."):
            continue
        if line:
            instructions.append(line)
    return instructions, labels


def register_index(name):
    if name not in REGISTERS:
        raise ValueError(f"unsupported register: {name}")
    return REGISTERS[name]


def run(value, instructions, labels):
    registers = [0] * 32
    registers[10] = value
    pc = 0
    count = 0
    branch_count = 0

    while True:
        fields = instructions[pc].replace(",", " ").split()
        operation = fields[0]
        count += 1
        if operation == "ret":
            break
        if operation == "beq":
            if registers[register_index(fields[1])] == registers[register_index(fields[2])]:
                pc = labels[fields[3].rstrip("f")]
            else:
                pc += 1
        elif operation == "bnez":
            if registers[register_index(fields[1])] != 0:
                pc = labels[fields[2].rstrip("f")]
            else:
                pc += 1
        elif operation == "addi":
            rd = register_index(fields[1])
            registers[rd] = (registers[register_index(fields[2])] + int(fields[3])) & 0xFFFFFFFF
            pc += 1
        elif operation in ("srli", "slli"):
            rd = register_index(fields[1])
            source = registers[register_index(fields[2])]
            amount = int(fields[3])
            registers[rd] = (
                source >> amount if operation == "srli" else (source << amount) & 0xFFFFFFFF
            )
            pc += 1
        else:
            raise ValueError(f"unsupported instruction: {operation}")
        registers[0] = 0
        if operation in BRANCHES:
            branch_count += 1

    return registers[10], count, branch_count


def main():
    instructions, labels = load_program()
    assert len(instructions) == 25
    assert sum(line.split()[0] in BRANCHES for line in instructions) == 6
    print("input        result  dynamic  branches")
    for value in TESTS:
        result, dynamic, branches = run(value, instructions, labels)
        assert result == EXPECTED[value]
        print(f"0x{value:08X}  {result:>6}  {dynamic:>8}  {branches:>8}")
    print("CP2 RV32I trace tests passed.")


if __name__ == "__main__":
    main()
