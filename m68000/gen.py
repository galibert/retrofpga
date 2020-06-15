from m68000 import m68000

from nmigen.back import rtlil

mod = m68000()

ports = [sig for attr, sig in vars(mod).items() if attr[:2] in ("i_", "o_")]

rtlil_text = rtlil.convert(mod, platform=None, name="m68000", ports=ports)
print("""
read_ilang <<rtlil
{}
rtlil
proc
flatten
memory_collect
opt -full
clean -purge
write_cxxrtl -O3
""".format(rtlil_text))
