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

gcc_support = 1
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
        with vsc.if_then(self.format.inside(vsc.rangelist(riscv_instr_format_t.CLB_FORMAT,
                                                          riscv_instr_format_t.CLH_FORMAT,
                                                          riscv_instr_format_t.CSH_FORMAT,
                                                          riscv_instr_format_t.CSB_FORMAT,
                                                          riscv_instr_format_t.CA_FORMAT,
                                                          riscv_instr_format_t.CSZN_FORMAT))):
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
        if self.format in [riscv_instr_format_t.CLB_FORMAT, riscv_instr_format_t.CSB_FORMAT]:
            self.imm_len = 2
        elif self.format in [riscv_instr_format_t.CLH_FORMAT, riscv_instr_format_t.CSH_FORMAT]:
             self.imm_len = 1

    def set_rand_mode(self):
        if self.format in [riscv_instr_format_t.CLB_FORMAT]:
            self.has_rs2 = 0
        elif self.instr_name in [riscv_instr_name_t.C_SB, riscv_instr_name_t.C_SH]:
            self.has_rd = 0
        elif self.instr_name in [riscv_instr_name_t.C_LHU, riscv_instr_name_t.C_LH]:
             self.has_rs2 = 0
        elif self.instr_name in [riscv_instr_name_t.C_ZEXT_B, riscv_instr_name_t.C_ZEXT_H, riscv_instr_name_t.C_ZEXT_W, riscv_instr_name_t.C_SEXT_B, riscv_instr_name_t.C_SEXT_H]:
            self.has_rs2 = 0
            self.has_rd = 0
            self.has_imm = 0
        elif self.format is riscv_instr_format_t.CA_FORMAT:
            self.has_rs1 = 0
            self.has_imm = 0


    
    

    def convert2asm(self, prefix=""):
        asm_str = pkg_ins.format_string(string=self.get_instr_name(),
                                        length=pkg_ins.MAX_INSTR_STR_LEN)
        binary = ''
        if self.category != riscv_instr_category_t.SYSTEM:
              
            if self.instr_name in [riscv_instr_name_t.C_LBU, riscv_instr_name_t.C_LHU, riscv_instr_name_t.C_LH]:
                asm_str = '{} {}, {}({})'.format(
                    asm_str, self.rd.name, self.get_imm(), self.rs1.name)
                if self.instr_name is riscv_instr_name_t.C_LBU:
                    binary = '.half {}{}{}{}{}{}'.format(self.get_func6(), self.get_reg(), self.imm[0], self.imm[1],self.get_reg(),self.get_c_opcode())
                elif self.instr_name is riscv_instr_name_t.C_LHU:
                    binary = '.half {}{}0{}{}{}'.format(self.get_func6(), self.get_reg(), self.imm[1], self.get_reg(), self.get_c_opcode())
                elif self.instr_name is riscv_instr_name_t.C_LH:
                    binary = '.half {}{}1{}{}{}'.format(self.get_func6(), self.get_reg(), self.imm[1], self.get_reg(), self.get_c_opcode())
            elif self.instr_name in [riscv_instr_name_t.C_SB, riscv_instr_name_t.C_SH]:
                    asm_str = '{} {}, {}({})'.format(
                        asm_str, self.rs2.name, self.get_imm(), self.rs1.name)
                    if self.instr_name is riscv_instr_name_t.C_SB:
                        binary = '.half {}{}{}{}{}{}'.format(self.get_func6(), self.get_reg(), self.imm[0], self.imm[1], self.get_reg(),self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_SH:
                        binary = '.half {}{}0{}{}{}'.format(self.get_func6(), self.get_reg(), self.imm[1],self.get_reg(), self.get_c_opcode())
            elif self.instr_name in [riscv_instr_name_t.C_ZEXT_B, riscv_instr_name_t.C_SEXT_B, riscv_instr_name_t.C_ZEXT_H, riscv_instr_name_t.C_SEXT_H, riscv_instr_name_t.C_ZEXT_W, riscv_instr_name_t.C_NOT]:
                    asm_str = '{} {}'.format(asm_str, self.rd.name)
                    if self.instr_name is riscv_instr_name_t.C_ZEXT_B:
                        binary = '.half {}{}11000{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_SEXT_B:
                        binary = '.half {}{}11001{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_ZEXT_H:
                        binary = '.half {}{}11010{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_SEXT_H:
                        binary = '.half {}{}11011{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_ZEXT_W:
                        binary = '.half {}{}11100{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
                    elif self.instr_name is riscv_instr_name_t.C_NOT:
                        binary = '.half {}{}11101{}'.format(self.get_func6(), self.get_reg(), self.get_c_opcode())
            elif self.instr_name is riscv_instr_name_t.C_MUL:
                    asm_str = '{} {}, {}'.format(asm_str, self.rd.name, self.rs2.name)
                    binary = '.half {}{}10{}{}'.format(self.get_func6(), self.get_reg(), self.get_reg(), self.get_c_opcode())
            else:
                logging.info("Unsupported format {}".format(self.format.name))

        if not gcc_support:
           asm_str = binary
        

        if self.comment != "":
            asm_str = asm_str + " #" + self.comment
        return asm_str.lower()
    

    def get_c_opcode(self):
    # Mapping of instruction names to their corresponding opcode
        opcode_map = {
            'C_ZEXT_B': '01', 'C_SEXT_B': '01', 'C_ZEXT_H': '01',
            'C_SEXT_H': '01', 'C_ZEXT_W': '01', 'C_NOT': '01', 'C_MUL': '01',
            'C_LBU': '00', 'C_LHU': '00', 'C_LH': '00', 'C_SB': '00', 'C_SH': '00',
        }

        # Retrieve the opcode based on the instruction name
        if self.instr_name in opcode_map:
            return opcode_map[self.instr_name]
        else:
            print(f"Unsupported instruction {self.instr_name}")


    def get_func6(self):
        # Mapping of instruction names to their corresponding func6 values
        func6_map = {
            'C_LBU': '100000', 'C_LHU': '100001', 'C_LH': '100001',
            'C_SB': '100010', 'C_SH': '100011', 'C_ZEXT_B': '100011',
            'C_SEXT_B': '100111', 'C_ZEXT_H': '100111', 'C_SEXT_H': '100111',
            'C_ZEXT_W': '100111', 'C_NOT': '100111', 'C_MUL': '100111',
        }

        # Retrieve the func6 value based on the instruction name
        if self.instr_name in func6_map:
            return func6_map[self.instr_name]
        else:
            print(f"Unsupported instruction {self.instr_name}")

    def get_reg(self):
        reg_map={
            'S0': '000', 
            'S1': '001', 
            'A0': '010',
            'A1': '011',
            'A2': '100',
            'A3': '101',            
            'A4': '110',
            'A5': '111',
        }

        if self.rs1.name in reg_map:
            return reg_map[self.rs1.name]
        elif self.rs2.name in reg_map:
            return reg_map[self.rs2.name]
        elif self.rd.name in reg_map:
            return reg_map[self.rd.name]
        else:
            print(f"Unsupported register name {self.instr_name}")