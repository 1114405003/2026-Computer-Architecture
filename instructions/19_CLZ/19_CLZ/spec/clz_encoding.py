"""CLZ custom instruction: encoding, golden model, and instruction-count comparison.

Instruction:  clz rd, rs1   ->   rd = CLZ(rs1)  (32-bit, result 0..32)
Format:       R-type on custom-0 opcode (0b0001011 = 0x0B)
              fun7/funct7 = 0, fun3/funct3 = 5, rs2 = 0 (ignored)
Fields:       7-bit fun7, 5-bit rs2, 5-bit rs1, 3-bit fun3,
              5-bit rd, 7-bit opcode
"""

OPCODE_CUSTOM0 = 0b0001011
FUNCT3_CLZ = 0b101
FUNCT7_CLZ = 0b0000000
MASK32 = 0xFFFFFFFF


def clz_golden(x: int) -> int:
    x &= MASK32
    if x == 0:
        return 32
    n = 0
    for i in range(31, -1, -1):
        if (x >> i) & 1:
            break
        n += 1
    return n


def encode_clz(rd: int, rs1: int, rs2: int = 0) -> int:
    for name, r in (("rd", rd), ("rs1", rs1), ("rs2", rs2)):
        if not 0 <= r <= 31:
            raise ValueError(f"{name} out of range: {r}")
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


def apply_clz(regs, rd: int, rs1: int) -> None:
    regs[0] = 0
    if rd == 0:
        return
    regs[rd] = clz_golden(regs[rs1])


def instruction_count_comparison():
    # Static RV32IM baseline (all instructions in clz.s) vs one custom instruction.
    rv32im_static = 25
    custom_static = 1
    samples = {
        0x80000000: 14,
        0x00010000: 21,
        0x00000001: 23,
        0x00000000: 3,
    }
    return {
        "rv32im_static": rv32im_static,
        "custom_static": custom_static,
        "dynamic_samples": samples,
        "dynamic_reduction": {
            x: round((v - 1) / v * 100, 1) for x, v in samples.items()
        },
    }


if __name__ == "__main__":
    word = encode_clz(10, 11, 0)  # clz a0, a1
    print(f"clz a0, a1  ->  0x{word:08x}  {word:032b}")
    print("decode:", decode_clz(word))
    for x in (0x80000000, 0x00010000, 0x00000001, 0x00000000, 0x00F00000):
        print(f"CLZ(0x{x:08X}) = {clz_golden(x)}")
    import pprint
    pprint.pprint(instruction_count_comparison())
