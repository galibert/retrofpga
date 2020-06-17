from nmigen import *

from eclock import eclock as _eclock
from idecode import idecode as _idecode
from microcode import microcode as _microcode

class m68000(Elaboratable):
    def __init__(self):
        self.i_pclk = Signal()
        self.i_nclk = Signal()

        self.o_micro  = Signal(17)
        self.o_nano   = Signal(68)

        self.i_eu_r = Signal()
        self.i_eu_w = Signal()

        self.i_ma   = Signal(10)

        self.o_e    = Signal()

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.eclock    = eclock    = _eclock()
        m.submodules.idecode   = idecode   = _idecode()
        m.submodules.microcode = microcode = _microcode()
        
        m.d.nclk += self.o_e.eq(eclock.o_e)

        m.d.comb += microcode.i_ma.eq(self.i_ma)
        m.d.comb += self.o_micro.eq(microcode.o_micro)
        m.d.comb += self.o_nano .eq(microcode.o_nano )
        
        m = EnableInserter({"pclk": self.i_pclk, "nclk": self.i_nclk})(m)
        m = EnableInserter({"eu_r": self.i_eu_r, "eu_w": self.i_eu_w})(m)
        m = DomainRenamer({"pclk": "sync", "nclk": "sync"})(m)
        m = DomainRenamer({"eu_r": "sync", "eu_w": "sync"})(m)
        return m
