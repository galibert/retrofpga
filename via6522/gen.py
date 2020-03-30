from via6522 import via6522

from nmigen.back import rtlil

mod = via6522()

ports = [sig for attr, sig in vars(mod).items() if attr[:2] in ("i_", "o_")]

rtlil_text = rtlil.convert(mod, platform=None, name="via6522", ports=ports)
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
