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

import sys
import logging
import vsc
from pygen_src.isa.riscv_instr import riscv_instr
from pygen_src.riscv_instr_pkg import (riscv_instr_name_t, riscv_instr_format_t,
                                       riscv_instr_category_t, riscv_reg_t, imm_t, pkg_ins)


@vsc.randobj
class riscv_zcb_instr(riscv_instr):
    def __init__(self):
        super().__init__()
        self.imm_align = 0
        self.rs1 = riscv_reg_t.S0
        self.rs2 = riscv_reg_t.S0
        self.rd = riscv_reg_t.S0
        self.is_compressed = 1
    
    @vsc.constraint
    def rvc_csr_c(self):
        #Registers specified by the three-bit rs1, rs2, and rd
        with vsc.if_then(self.format.inside(vsc.rangelist(riscv_instr_format_t.CIW_FORMAT,
                                                          riscv_instr_format_t.CL_FORMAT,
                                                          riscv_instr_format_t.CS_FORMAT,
                                                          riscv_instr_format_t.CB_FORMAT,
                                                          riscv_instr_format_t.CA_FORMAT,
                                                          riscv_instr_format_t.CE_FORMAT))):
            with vsc.if_then(self.has_rs1 == 1):
                self.rs1.inside(vsc.rangelist(riscv_reg_t.S0, riscv_reg_t.S1, riscv_reg_t.A0,
                                              riscv_reg_t.A1, riscv_reg_t.A2, riscv_reg_t.A3,
                                              riscv_reg_t.A4, riscv_reg_t.A5))
            with vsc.if_then(self.has_rs2 == 1):
                self.rs2.inside(vsc.rangelist(riscv_reg_t.S0, riscv_reg_t.S1, riscv_reg_t.A0,
                                              riscv_reg_t.A1, riscv_reg_t.A2, riscv_reg_t.A3,
                                              riscv_reg_t.A4, riscv_reg_t.A5))
            with vsc.if_then(self.has_rd == 1):
                self.rd.inside(vsc.rangelist(riscv_reg_t.S0, riscv_reg_t.S1, riscv_reg_t.A0,
                                             riscv_reg_t.A1, riscv_reg_t.A2, riscv_reg_t.A3,
                                             riscv_reg_t.A4, riscv_reg_t.A5))

    @vsc.constraint
    def imm_val_c(self):
        with vsc.if_then(self.instr_name.inside(vsc.rangelist(riscv_instr_name_t.C_LBU,
                                                                  riscv_instr_name_t.C_LHU,
                                                                  riscv_instr_name_t.C_LH,
                                                                  riscv_instr_name_t.C_SB))):
                self.imm[31:2] == 0
                with vsc.if_then(self.instr_name.inside(vsc.rangelist(riscv_instr_name_t.C_LHU,
                                                                      riscv_instr_name_t.C_SH))):
                    self.imm[0] == 0
                with vsc.if_then(self.instr_name.inside(vsc.rangelist(riscv_instr_name_t.C_LH))):
                    self.imm[0] == 1
        
    def set_imm_len(self):
        if self.format in [riscv_instr_format_t.CL_FORMAT, riscv_instr_format_t.CS_FORMAT]:
            self.imm_len = 5

    def set_rand_mode(self):
        if self.format in [riscv_instr_format_t.CL_FORMAT]:
            self.has_rs2 = 0
        elif self.format in [riscv_instr_format_t.CS_FORMAT]:
            self.has_rd = 0
        elif self.format in [riscv_instr_format_t.CA_FORMAT, riscv_instr_format_t.CE_FORMAT]:
            self.has_rs1 = 0
            self.has_imm = 0


    
    

    def convert2asm(self, prefix=""):
        asm_str = pkg_ins.format_string(string=self.get_instr_name(),
                                        length=pkg_ins.MAX_INSTR_STR_LEN)
        if self.category != riscv_instr_category_t.SYSTEM:
              
            if self.instr_name in [riscv_instr_name_t.C_LBU, riscv_instr_name_t.C_LHU, riscv_instr_name_t.C_LH]:
                asm_str = '{} {}, {}({})'.format(
                    asm_str, self.rd.name, self.get_imm(), self.rs1.name)
            elif self.instr_name in [riscv_instr_name_t.C_SB, riscv_instr_name_t.C_SH]:
                #if self.category is riscv_instr_category_t.STORE:
                    asm_str = '{} {}, {}({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
            elif self.instr_name in [riscv_instr_name_t.C_ZEXT_B, riscv_instr_name_t.C_SEXT_B, riscv_instr_name_t.C_ZEXT_H, riscv_instr_name_t.C_SEXT_H, riscv_instr_name_t.C_ZEXT_W, riscv_instr_name_t.C_NOT]:
                    asm_str = '{} {}'.format(asm_str, self.rd.name)
            elif self.instr_name is riscv_instr_name_t.C_MUL:
                    asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.rs2.name)
            else:
                logging.info("Unsupported format {}".format(self.format.name))

        if self.comment != "":
            asm_str = asm_str + " #" + self.comment
        return asm_str.lower()
    

    