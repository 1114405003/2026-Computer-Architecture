"""CLZ custom instruction: encoding, golden model, and instruction counts.

Instruction:  clz rd, rs1   ->   rd = CLZ(rs1)  (32-bit, result 0..32)
Format:       R-type on custom-0 opcode (0b0001011 = 0x0B)
              funct7 = 0b0000000, funct3 = 0b000, rs2 = 0 (ignored)
Fields:       7-bit funct7, 5-bit rs2, 5-bit rs1, 3-bit funct3,
              5-bit rd, 7-bit opcode
"""

OPCODE_CUSTOM0 = 0b0001011
FUNCT3_CLZ = 0b000
FUNCT7_CLZ = 0b0000000
MASK32 = 0xFFFFFFFF


def clz_golden(value: int) -> int:
    value &= MASK32
    if value == 0:
        return 32
    return 32 - value.bit_length()


def encode_clz(rd: int, rs1: int, rs2: int = 0) -> int:
    for name, register in (("rd", rd), ("rs1", rs1), ("rs2", rs2)):
        if not 0 <= register <= 31:
            raise ValueError(f"{name} out of range: {register}")
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


def instruction_count_comparison():
    """Static counts plus the four dynamic samples produced by cp2_trace.py."""
    samples = {
        0x80000000: 14,
        0x00010000: 21,
        0x00000001: 23,
        0x00000000: 3,
    }
    return {
        "rv32im_binary_search_static": 25,
        "rv32im_bit_loop_static": 11,
        "custom_static": 1,
        "dynamic_samples": samples,
        "dynamic_reduction_percent": {
            value: round((count - 1) / count * 100, 1)
            for value, count in samples.items()
        },
    }


if __name__ == "__main__":
    for rd, rs1 in ((10, 11), (5, 6), (1, 2)):
        word = encode_clz(rd, rs1)
        print(
            f"clz x{rd}, x{rs1}  ->  0x{word:08X}  {word:032b}  "
            f"decode={decode_clz(word)}"
        )

    print()
    for value in (0x80000000, 0x00010000, 0x00000001, 0x00000000, 0x00F00000):
        print(f"CLZ(0x{value:08X}) = {clz_golden(value)}")

    print()
    import pprint

    pprint.pprint(instruction_count_comparison())
