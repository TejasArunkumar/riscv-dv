import sys
import logging
import vsc
from pygen_src.isa.riscv_instr import riscv_instr
from pygen_src.riscv_instr_pkg import pkg_ins, riscv_instr_name_t, riscv_instr_group_t

#list_zicbom = ["cbo.clean","cbo.flush","cbo.inval"]
#list_zicbop = ["prefetch.i","prefetch.r","prefetch.w"]
#list_z = ["cbo.clean","cbo.flush","cbo.inval","prefetch.i","prefetch.r","prefetch.w"]
@vsc.randobj
class riscv_cache_instr(riscv_instr):
    def __init__(self):
        super().__init__()
        self.has_offset = vsc.rand_bit_t(1)
        logging.info("const being called")
        

    def get_instr_name(self):
        get_instr_name = self.instr_name.name
        #self.group == riscv_instr_group_t.RV32Z:
        logging.info("get name being called") 
        '''
        else:
            logging.critical("Unexpected Z instr group: {} / {}"
                             .format(self.group.name, self.instr_name.name))
            sys.exit(1)
            '''
        return get_instr_name

    # Convert the instruction to assembly code
    def convert2asm(self, prefix = ""):
        asm_str = pkg_ins.format_string(self.get_instr_name(), pkg_ins.MAX_INSTR_STR_LEN)
        if self.group in [riscv_instr_group_t.RV32Z]:
             asm_str = "{} {}({})".format(asm_str,self.get_imm(), self.rs1.name)
             logging.info(" ASM gen being run")
        else:
            logging.critical("Unexpected Z instr group: {} / {}"
                             .format(self.group.name, self.instr_name.name))
            sys.exit(1)
        
        return asm_str.lower()
