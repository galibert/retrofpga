import sys
sys.path.append('..')

from k053252 import k053252
from nmigen.back import rtlil

rtlil_text = rtlil.convert(k053252.k053252(), platform=None, name="overdrive")
print("""
read_ilang <<rtlil
{}
rtlil
proc
expose w:o_* w:*$next %d
opt -full
clean -purge
write_cxxrtl
""".format(rtlil_text))
