#include "clz_wrapper.h"

uint32_t clz_via_wrapper(uint32_t x)
{
    return clz_insn(x);
}
