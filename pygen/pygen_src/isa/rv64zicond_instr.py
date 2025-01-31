"""
Copyright 2020 Google LLC
Copyright 2020 PerfectVIPs Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""

from pygen_src.riscv_defines import DEFINE_ZICOND_INSTR
from pygen_src.riscv_instr_pkg import (riscv_instr_name_t, riscv_instr_format_t,
                                       riscv_instr_category_t, riscv_instr_group_t, imm_t)

DEFINE_ZICOND_INSTR(riscv_instr_name_t.CZERO_EQZ, riscv_instr_format_t.R_FORMAT,
                    riscv_instr_category_t.COMPARE, riscv_instr_group_t.RV64Zicond, g=globals())
DEFINE_ZICOND_INSTR(riscv_instr_name_t.CZERO_NEZ, riscv_instr_format_t.R_FORMAT,
                    riscv_instr_category_t.COMPARE, riscv_instr_group_t.RV64Zicond, g=globals())