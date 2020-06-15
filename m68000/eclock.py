from nmigen import *

class eclock(Elaboratable):
    def __init__(self):
        self.o_e    = Signal()

        self.estate = Signal(4)
        self.elfsr  = Signal(4)
        self.enlfsr = Signal(4)
        self.ereset = Signal()
        self.ein    = Signal()
        

    def elaborate(self, platform):
        m = Module()

        with m.If(self.ereset):
            m.d.comb += self.estate.eq(0)
        with m.Else():
            m.d.comb += self.estate.eq(~self.elfsr)

        m.d.pclk += self.enlfsr.eq(self.estate)
        m.d.nclk += self.elfsr[0].eq(self.ein)
        m.d.nclk += self.elfsr[1:4].eq(~self.enlfsr[0:3])
        m.d.pclk += self.ein.eq(self.estate[2] ^ self.estate[3])
        m.d.pclk += self.ereset.eq((self.estate == 9) | (self.estate == 0xf))

        with m.If(self.estate == 7):
            m.d.pclk += self.o_e.eq(0)
        with m.Elif(self.estate == 9):
            m.d.pclk += self.o_e.eq(1)
        
        return m
