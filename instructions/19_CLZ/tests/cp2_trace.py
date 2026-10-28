"""RV32I instruction-level trace runner for the CP2 CLZ baselines.

This is not Spike or Ripes.  It executes the exact instructions contained in
src/rv32im/clz.s and src/rv32im/clz_loop.s and reports the number of executed
instructions and conditional branches.  The same runner is used to produce
tests/cp2_trace_output.txt and tests/cp2_trace_detail.txt.

Environment used for the submitted output:
    Python 3.12.10 on Windows
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY_ASM = ROOT / "src" / "rv32im" / "clz.s"
LOOP_ASM = ROOT / "src" / "rv32im" / "clz_loop.s"

TESTS = (
    0x80000000,
    0x40000000,
    0x20000000,
    0x10000000,
    0x08000000,
    0x01000000,
    0x00100000,
    0x00010000,
    0x00000001,
    0x00000000,
    0x00F00000,
    0x0000FFFF,
)

EXPECTED = {
    0x80000000: 0,
    0x40000000: 1,
    0x20000000: 2,
    0x10000000: 3,
    0x08000000: 4,
    0x01000000: 7,
    0x00100000: 11,
    0x00010000: 15,
    0x00000001: 31,
    0x00000000: 32,
    0x00F00000: 8,
    0x0000FFFF: 16,
}

MASK32 = 0xFFFFFFFF
REGISTERS = {"zero": 0, "ra": 1, "a0": 10, "t0": 5, "t1": 6, "t2": 7}
CONDITIONAL_BRANCHES = {"beq", "bnez"}


def parse_program(path: Path) -> tuple[list[str], dict[str, int]]:
    """Return (instruction list, label -> instruction index)."""
    instructions: list[str] = []
    labels: dict[str, int] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith(".") and ":" not in line:
            continue
        if ":" in line:
            label, rest = line.split(":", 1)
            labels[label.strip()] = len(instructions)
            line = rest.strip()
            if not line:
                continue
        instructions.append(line)
    return instructions, labels


def register_index(name: str) -> int:
    if name not in REGISTERS:
        raise ValueError(f"unsupported register: {name}")
    return REGISTERS[name]


def is_conditional_branch(instruction: str) -> bool:
    return instruction.split()[0] in CONDITIONAL_BRANCHES


def static_branch_count(instructions: list[str]) -> int:
    return sum(is_conditional_branch(insn) for insn in instructions)


def run(
    instructions: list[str],
    labels: dict[str, int],
    value: int,
    record_trace: bool = False,
) -> tuple[int, int, int, list[tuple[int, int, str, int, int, int]]]:
    """Execute one CLZ call and return (result, dynamic, branches, trace)."""
    registers = [0] * 32
    registers[10] = value & MASK32
    pc = 0
    dynamic = 0
    branches = 0
    trace: list[tuple[int, int, str, int, int, int]] = []

    while True:
        if pc < 0 or pc >= len(instructions):
            raise RuntimeError(f"PC out of range: {pc}")
        text = instructions[pc]
        fields = text.replace(",", " ").split()
        operation = fields[0]

        if record_trace:
            trace.append(
                (dynamic + 1, pc, text, registers[10], registers[5], registers[6])
            )

        dynamic += 1

        if operation == "ret":
            break
        if operation == "beq":
            branches += 1
            if registers[register_index(fields[1])] == registers[register_index(fields[2])]:
                pc = labels[fields[3]]
            else:
                pc += 1
        elif operation == "bnez":
            branches += 1
            if registers[register_index(fields[1])] != 0:
                pc = labels[fields[2]]
            else:
                pc += 1
        elif operation == "jal":
            # Only "jal zero, label" is used by the baselines.
            pc = labels[fields[2]]
        elif operation == "j":
            pc = labels[fields[1]]
        elif operation == "addi":
            rd = register_index(fields[1])
            registers[rd] = (
                registers[register_index(fields[2])] + int(fields[3], 0)
            ) & MASK32
            pc += 1
        elif operation in ("srli", "slli"):
            rd = register_index(fields[1])
            source = registers[register_index(fields[2])]
            amount = int(fields[3], 0)
            registers[rd] = (
                (source >> amount)
                if operation == "srli"
                else ((source << amount) & MASK32)
            )
            pc += 1
        else:
            raise ValueError(f"unsupported instruction: {text}")

        registers[0] = 0

    return registers[10], dynamic, branches, trace


def print_detail(name: str, instructions: list[str], labels: dict[str, int], value: int) -> None:
    result, dynamic, branches, trace = run(instructions, labels, value, record_trace=True)
    print(f"\nDetail trace: {name}, input=0x{value:08X}, result={result}, "
          f"dynamic={dynamic}, branches={branches}")
    print("step  pc  instruction                 a0          t0  t1")
    for step, pc, text, a0, t0, t1 in trace:
        print(f"{step:4d} {pc:3d}  {text:<26} 0x{a0:08X} {t0:3d} {t1:3d}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--detail",
        type=lambda text: int(text, 0),
        metavar="VALUE",
        help="print a per-instruction trace for one input, e.g. --detail 0x00010000",
    )
    args = parser.parse_args()

    binary_instructions, binary_labels = parse_program(BINARY_ASM)
    loop_instructions, loop_labels = parse_program(LOOP_ASM)

    assert len(binary_instructions) == 25, "clz.s static instruction count changed"
    assert static_branch_count(binary_instructions) == 6, "clz.s static branch count changed"
    assert len(loop_instructions) == 11, "clz_loop.s static instruction count changed"
    assert static_branch_count(loop_instructions) == 2, "clz_loop.s static branch count changed"

    print("input        result   clz.s dyn  clz.s br  loop dyn  loop br")
    for value in TESTS:
        binary_result, binary_dynamic, binary_branches, _ = run(
            binary_instructions, binary_labels, value
        )
        loop_result, loop_dynamic, loop_branches, _ = run(
            loop_instructions, loop_labels, value
        )
        assert binary_result == EXPECTED[value], f"clz.s failed for 0x{value:08X}"
        assert loop_result == EXPECTED[value], f"clz_loop.s failed for 0x{value:08X}"
        print(
            f"0x{value:08X}  {binary_result:>6}  {binary_dynamic:>9}  "
            f"{binary_branches:>8}  {loop_dynamic:>8}  {loop_branches:>7}"
        )

    if args.detail is not None:
        print_detail("clz.s", binary_instructions, binary_labels, args.detail)
        print_detail("clz_loop.s", loop_instructions, loop_labels, args.detail)

    print("\nStatic instructions: clz.s = 25, clz_loop.s = 11")
    print("Static conditional branches: clz.s = 6, clz_loop.s = 2")
    print("CP2 RV32I trace tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
