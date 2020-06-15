from nmigen import *

class eclock(Elaboratable):
    def __init__(self):
        self.o_e    = Signal()

        self.estate = Signal(4)
        self.elsfr  = Signal(4)
        self.enlsfr = Signal(4)
        self.ereset = Signal()
        self.ein    = Signal()
        

    def elaborate(self, platform):
        m = Module()

        with m.If(self.ereset):
            m.d.comb += self.estate.eq(0)
        with m.Else():
            m.d.comb += self.estate.eq(~self.elsfr)

        m.d.pclk += self.enlsfr.eq(self.estate)
        m.d.nclk += self.elsfr[0].eq(self.ein)
        m.d.nclk += self.elsfr[1:4].eq(~self.enlsfr[1:4])
        m.d.pclk += self.ein.eq(self.estate[2] ^ self.estate[3])
        m.d.pclk += self.ereset.eq((self.estate == 6) | (self.estate == 0))

        with m.If(self.estate == 7):
            m.d.pclk += self.o_e.eq(0)
        with m.Elif(self.estate == 9):
            m.d.pclk += self.o_e.eq(1)
        
        return m
