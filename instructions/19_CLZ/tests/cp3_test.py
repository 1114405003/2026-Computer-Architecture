"""CP3 CLZ semantic and instruction-encoding tests."""

TEST_VECTORS = (
    (0x80000000, 0, "highest bit is one"),
    (0x40000000, 1, "one leading zero"),
    (0x00010000, 15, "16-bit boundary"),
    (0x00000001, 31, "lowest bit is one"),
    (0x00000000, 32, "zero special case"),
)

OPCODE_CUSTOM0 = 0x0B
FUNCT3_CLZ = 0b101
FUNCT7_CLZ = 0


def clz_golden(value):
    value &= 0xFFFFFFFF
    if value == 0:
        return 32
    return 32 - value.bit_length()


def encode_clz(rd, rs1, rs2=0):
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


def decode_clz(word):
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


def main():
    passed = 0
    for index, (value, expected, description) in enumerate(TEST_VECTORS, 1):
        actual = clz_golden(value)
        result = "PASS" if actual == expected else "FAIL"
        print(
            f"Test {index}: CLZ(0x{value:08X}) = {actual} "
            f"(expected {expected}) {result} - {description}"
        )
        passed += actual == expected

    encoded = encode_clz(rd=10, rs1=11)
    decoded = decode_clz(encoded)
    encoding_ok = encoded == 0x0005D50B and decoded == {
        "rd": 10,
        "rs1": 11,
        "rs2": 0,
    }
    print(
        f"Encoding: clz x10, x11 = 0x{encoded:08X} "
        f"({'PASS' if encoding_ok else 'FAIL'})"
    )
    passed += encoding_ok

    total = len(TEST_VECTORS) + 1
    print(f"{passed}/{total} CP3 tests passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
