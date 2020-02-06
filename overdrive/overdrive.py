import sys
sys.path.append('..')

from k053252 import k053252
from nmigen import *
from nmigen.back import rtlil

class overdrive(Elaboratable):
    def __init__(self):
        self.o_nhsy = Signal()
        self.o_nhbk = Signal()
        self.o_nvsy = Signal()
        self.o_nvbk = Signal()

        self.m_timings = k053252.k053252()

    def elaborate(self, platform):
        m = Module()
        m.submodules += self.m_timings
        m.d.comb += self.o_nhsy.eq(self.m_timings.o_nhsy)
        m.d.comb += self.o_nvsy.eq(self.m_timings.o_nvsy)
        m.d.comb += self.o_nhbk.eq(self.m_timings.o_nhbk)
        m.d.comb += self.o_nvbk.eq(self.m_timings.o_nvbk)
        return m



rtlil_text = rtlil.convert(overdrive(), platform=None, name="overdrive")
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
