from nmigen import *

from eclock import eclock as _eclock
from idecode import idecode as _idecode

class m68000(Elaboratable):
    def __init__(self):
        self.i_pclk = Signal()
        self.i_nclk = Signal()

        self.i_ird  = Signal(16)
        self.o_ma1  = Signal(10)

        self.o_e    = Signal()

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.eclock  = eclock  = _eclock()
        m.submodules.idecode = idecode = _idecode()
        
        m.d.nclk += self.o_e.eq(eclock.o_e)

        m.d.pclk += idecode.i_ird.eq(self.i_ird)
        m.d.nclk += self.o_ma1.eq(idecode.o_ma1)
        
        m = EnableInserter({"pclk": self.i_pclk, "nclk": self.i_nclk})(m)
        m = DomainRenamer({"pclk": "sync", "nclk": "sync"})(m)
        return m
