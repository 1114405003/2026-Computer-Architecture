"""CP3 CLZ semantic and instruction-encoding tests.

Encoding follows the course announcement:
    custom-0 opcode = 0b0001011, funct3 = 0b000, funct7 = 0b0000000.
"""

TEST_VECTORS = (
    (0x80000000, 0, "highest bit is one"),
    (0x40000000, 1, "one leading zero"),
    (0x00010000, 15, "16-bit boundary"),
    (0x00000001, 31, "lowest bit is one"),
    (0x00000000, 32, "zero special case"),
)

# (rd, rs1, expected machine code) for "clz rd, rs1".
EXAMPLES = (
    (10, 11, 0x0005850B),
    (5, 6, 0x0003028B),
    (1, 2, 0x0001008B),
)

OPCODE_CUSTOM0 = 0x0B
FUNCT3_CLZ = 0b000
FUNCT7_CLZ = 0b0000000
MASK32 = 0xFFFFFFFF


def clz_golden(value: int) -> int:
    value &= MASK32
    if value == 0:
        return 32
    return 32 - value.bit_length()


def encode_clz(rd: int, rs1: int, rs2: int = 0) -> int:
    if not all(0 <= register <= 31 for register in (rd, rs1, rs2)):
        raise ValueError("register number must be in the range 0..31")
    return (
        (FUNCT7_CLZ << 25)
        | (rs2 << 20)
        | (rs1 << 15)
        | (FUNCT3_CLZ << 12)
        | (rd << 7)
        | OPCODE_CUSTOM0
    )


def decode_clz(word: int):
    if word & 0x7F != OPCODE_CUSTOM0:
        return None
    if (word >> 25) & 0x7F != FUNCT7_CLZ:
        return None
    if (word >> 12) & 0x7 != FUNCT3_CLZ:
        return None
    return {
        "rd": (word >> 7) & 0x1F,
        "rs1": (word >> 15) & 0x1F,
        "rs2": (word >> 20) & 0x1F,
    }


def apply_clz(registers: list[int], rd: int, rs1: int) -> None:
    registers[0] = 0
    if rd == 0:
        return
    registers[rd] = clz_golden(registers[rs1])


def main() -> int:
    passed = 0
    total = 0

    for index, (value, expected, description) in enumerate(TEST_VECTORS, 1):
        actual = clz_golden(value)
        ok = actual == expected
        print(
            f"Test {index}: CLZ(0x{value:08X}) = {actual} "
            f"(expected {expected}) {'PASS' if ok else 'FAIL'} - {description}"
        )
        passed += ok
        total += 1

    for rd, rs1, expected_word in EXAMPLES:
        word = encode_clz(rd=rd, rs1=rs1)
        decoded = decode_clz(word)
        ok = (
            word == expected_word
            and decoded == {"rd": rd, "rs1": rs1, "rs2": 0}
        )
        print(
            f"Encoding: clz x{rd}, x{rs1} = 0x{word:08X} "
            f"(expected 0x{expected_word:08X}) {'PASS' if ok else 'FAIL'}"
        )
        passed += ok
        total += 1

    registers = [0] * 32
    registers[5] = 123
    apply_clz(registers, rd=0, rs1=5)
    rd_zero_ok = registers[0] == 0 and registers[5] == 123
    print(f"rd = x0 leaves the register file unchanged: {'PASS' if rd_zero_ok else 'FAIL'}")
    passed += rd_zero_ok
    total += 1

    print(f"{passed}/{total} CP3 tests passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
