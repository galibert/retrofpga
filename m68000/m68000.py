from nmigen import *

from eclock import eclock as _eclock

class m68000(Elaboratable):
    def __init__(self):
        self.i_pclk = Signal()
        self.i_nclk = Signal()

        self.o_e    = Signal()

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.eclock = eclock = _eclock()
 
        m.d.nclk += self.o_e.eq(eclock.o_e)

        m = EnableInserter({"pclk": self.i_pclk, "nclk": self.i_nclk})(m)
        m = DomainRenamer({"pclk": "sync", "nclk": "sync"})(m)
        return m
