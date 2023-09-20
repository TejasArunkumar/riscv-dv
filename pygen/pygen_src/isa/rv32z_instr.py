
from pygen_src.riscv_defines import DEFINE_INSTR
from pygen_src.riscv_instr_pkg import (riscv_instr_name_t, riscv_instr_format_t,
                                       riscv_instr_category_t, riscv_instr_group_t, imm_t)


DEFINE_INSTR(riscv_instr_name_t.CBO_CLEAN, riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())
DEFINE_INSTR(riscv_instr_name_t.CBO_FLUSH, riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())
DEFINE_INSTR(riscv_instr_name_t.CBO_INVAL, riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())
DEFINE_INSTR(riscv_instr_name_t.PREFETCH_I, riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())
DEFINE_INSTR(riscv_instr_name_t.PREFETCH_R, riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())
DEFINE_INSTR(riscv_instr_name_t.PREFETCH_W ,riscv_instr_format_t.Z_FORMAT,
             riscv_instr_category_t.CACHE, riscv_instr_group_t.RV32Z, g=globals())