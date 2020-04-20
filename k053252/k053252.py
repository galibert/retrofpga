from nmigen import *
from enum import IntEnum

class smode(IntEnum):
    front = 0
    sync  = 1
    back  = 2
    vis   = 3

class k053252(Elaboratable):
    def __init__(self):
        self.i_clkp  = Signal()
        
        self.i_ab    = Signal(4)
        self.i_db    = Signal(8)
        self.i_ccs   = Signal()
        self.i_rw    = Signal()

        self.o_db    = Signal(8)
        self.o_ncsy  = Signal()
        self.o_ncbk  = Signal()
        self.o_nhsy  = Signal()
        self.o_nhbk  = Signal()
        self.o_nvsy  = Signal()
        self.o_nvbk  = Signal()
        self.o_int1  = Signal()
        self.o_int2  = Signal()
        self.o_fcnt  = Signal()

        self.o_clk1p = Signal()
        self.o_clk1n = Signal()
        self.o_clk2p = Signal()
        self.o_clk2n = Signal()
        self.o_clk3p = Signal()
        self.o_clk3n = Signal()
        self.o_clk4p = Signal()
        self.o_clk4n = Signal()
        self.o_pep   = Signal()
        self.o_pen   = Signal()
        self.o_pqp   = Signal()
        self.o_pqn   = Signal()
        
        self.hc       = Signal(10, reset = 0x17f)
        self.hfp      = Signal( 9, reset = 0x010)
        self.hbp      = Signal( 9, reset = 0x030)
        self.vc       = Signal( 9, reset = 0x107)
        self.vfp      = Signal( 8, reset =  0x11)
        self.vbp      = Signal( 8, reset =  0x0e)
        self.vsw      = Signal( 4, reset =   0x7)
        self.hsw      = Signal( 4, reset =   0x3)
        self.int_time = Signal( 8, reset =  0xff)
        self.hct      = Signal(10, reset = 0x000)
        self.hctf     = Signal( 9, reset = 0x001)
        self.vct      = Signal( 9, reset = 0x001)
        self.vctf     = Signal( 8, reset =  0x01)
        self.hm       = Signal(smode, reset = smode.front)
        self.vm       = Signal(smode, reset = smode.front)
        self.fc       = Signal(2, reset = 0)
        self.clki     = Signal(3, reset = 0)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.o_ncsy.eq(self.o_nhsy & self.o_nvsy)
        m.d.comb += self.o_ncbk.eq(self.o_nhbk & self.o_nvbk)
        m.d.comb += self.o_nhsy.eq(self.hm != smode.sync)
        m.d.comb += self.o_nvsy.eq(self.vm != smode.sync)
        m.d.comb += self.o_nhbk.eq(self.hm == smode.vis)
        m.d.comb += self.o_nvbk.eq(self.vm == smode.vis)
        m.d.comb += self.o_fcnt.eq(self.fc[1])
        m.d.comb += self.o_clk1p.eq(self.clki[:1] == 0)
        m.d.comb += self.o_clk1n.eq(self.clki[:1] == 1)
        m.d.comb += self.o_clk2p.eq(self.clki[:2] == 0)
        m.d.comb += self.o_clk2n.eq(self.clki[:2] == 2)
        m.d.comb += self.o_clk3p.eq(self.clki[:3] == 0)
        m.d.comb += self.o_clk3n.eq(self.clki[:3] == 4)
        m.d.comb += self.o_clk4p.eq(self.clki[:2] == 1)
        m.d.comb += self.o_clk4n.eq(self.clki[:2] == 3)
        m.d.comb += self.o_clk3p.eq(self.clki[:3] == 0)
        m.d.comb += self.o_clk3n.eq(self.clki[:3] == 4)
        m.d.comb += self.o_pep  .eq(self.clki[:3] == 1)
        m.d.comb += self.o_pen  .eq(self.clki[:3] == 5)
        m.d.comb += self.o_pqp  .eq(self.clki[:3] == 3)
        m.d.comb += self.o_pqn  .eq(self.clki[:3] == 7)

        with m.If(self.i_clkp):
            m.d.sync += self.clki.eq(self.clki + 1)

        with m.If(self.o_clk2p):
            hend  = Signal()
            vend  = Signal()
            hstep = Signal()
            vstep = Signal()
            m.d.comb += hend.eq(self.hct == self.hc)
            m.d.comb += vend.eq(self.vct == self.vc)
            with m.Switch(self.hm):
                with m.Case(smode.front):
                    m.d.comb += hstep.eq(self.hctf == self.hfp)
                with m.Case(smode.sync):
                    m.d.comb += hstep.eq(self.hctf[3:7] == self.hsw)
                with m.Case(smode.back):
                    m.d.comb += hstep.eq(self.hctf == self.hbp)
                with m.Case(smode.vis):
                    m.d.comb += hstep.eq(0)
            with m.Switch(self.vm):
                with m.Case(smode.front):
                    m.d.comb += vstep.eq(self.vctf == self.vfp)
                with m.Case(smode.sync):
                    m.d.comb += vstep.eq(self.vctf[0:4] == self.vsw)
                with m.Case(smode.back):
                    m.d.comb += vstep.eq(self.vctf == self.vbp)
                with m.Case(smode.vis):
                    m.d.comb += vstep.eq(0)

            with m.If(hend):
                m.d.sync += self.hm.eq(smode.front)
                m.d.sync += self.hct.eq(1)
                m.d.sync += self.hctf.eq(2)
                with m.If(vend):
                    m.d.sync += self.vm.eq(smode.front)
                    m.d.sync += self.vct.eq(1)
                    m.d.sync += self.vctf.eq(1)
                    m.d.sync += self.o_int1.eq(0)
                    m.d.sync += self.fc.eq(self.fc + 1)
                with m.Elif(vstep):
                    with m.Switch(self.vm):
                        with m.Case(smode.front):
                            m.d.sync += [self.vctf.eq(1), self.vm.eq(smode.sync)]
                        with m.Case(smode.sync):
                            m.d.sync += [self.vctf.eq(1), self.vm.eq(smode.back)]
                        with m.Case(smode.back):
                            m.d.sync += [self.vctf.eq(0), self.vm.eq(smode.vis)]
                    m.d.sync += self.vct.eq(self.vct + 1)
                with m.Else():
                    m.d.sync += self.vct.eq(self.vct + 1)
                    m.d.sync += self.vctf.eq(self.vctf + 1)
            with m.Elif(hstep):
                with m.Switch(self.hm):
                    with m.Case(smode.front):
                        m.d.sync += [self.hctf.eq(1), self.hm.eq(smode.sync)]
                    with m.Case(smode.sync):
                        m.d.sync += [self.hctf.eq(0), self.hm.eq(smode.back)]
                    with m.Case(smode.back):
                        m.d.sync += [self.hctf.eq(0), self.hm.eq(smode.vis)]
                m.d.sync += self.hct.eq(self.hct + 1)
            with m.Else():
                m.d.sync += self.hct.eq(self.hct + 1)
                m.d.sync += self.hctf.eq(self.hctf + 1)

        with m.Elif(self.o_clk2n):
            with m.If(self.i_ccs == 0):
                with m.If(self.i_rw):
                    with m.If(self.i_ab == 0xe):
                        m.d.sync += [self.o_db[1:].eq(0x7f), self.o_db[0 ].eq(self.vct[8])]
                    with m.Elif(self.i_ab == 0xf):
                        m.d.sync += self.o_db.eq(self.vct[:8])
                    with m.Else():
                        m.d.sync += self.o_db.eq(0xff)
                with m.Else():
                    m.d.sync += self.o_db.eq(0xff)
                    with m.Switch(self.i_ab):
                        with m.Case(0x0):
                            m.d.sync += self.hc[8:].eq(self.i_db[:2])
                        with m.Case(0x1):
                            m.d.sync += self.hc[:8].eq(self.i_db)
                        with m.Case(0x2):
                            m.d.sync += self.hfp[8:].eq(self.i_db[0])
                        with m.Case(0x3):
                            m.d.sync += self.hfp[:8].eq(self.i_db)
                        with m.Case(0x4):
                            m.d.sync += self.hbp[8:].eq(self.i_db[0])
                        with m.Case(0x5):
                            m.d.sync += self.hbp[:8].eq(self.i_db)
                        with m.Case(0x8):
                            m.d.sync += self.vc[8:].eq(self.i_db[0])
                        with m.Case(0x9):
                            m.d.sync += self.vc[:8].eq(self.i_db)
                        with m.Case(0xa):
                            m.d.sync += self.vfp.eq(self.i_db)
                        with m.Case(0xb):
                            m.d.sync += self.vbp.eq(self.i_db)
                        with m.Case(0xc):
                            m.d.sync += self.vsw.eq(self.i_db[4:])
                            m.d.sync += self.hsw.eq(self.i_db[:4])
                        with m.Case(0xe):
                            m.d.sync += self.o_int1.eq(1)
                        with m.Case(0xf):
                            m.d.sync += self.o_int2.eq(1)
            with m.Else():
                m.d.sync += self.o_db.eq(0xff)
            
        return m
