from overdrive import overdrive

from nmigen.back import rtlil

mod = overdrive()
ports = [sig for attr, sig in vars(mod).items() if attr[:2] in ("i_", "o_")]

rtlil_text = rtlil.convert(mod, platform=None, name="overdrive", ports=ports)
print("""
read_ilang <<rtlil
{}
rtlil
proc
flatten
memory_collect
opt -full
clean -purge
write_cxxrtl -O0
""".format(rtlil_text))
