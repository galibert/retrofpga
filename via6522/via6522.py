from nmigen import *

# Chip has one clock, phi2.  Three clocks signals are generated from it
# - phi2 itself (p1)
# - iclk_pulse, a small length pulse on transition on phi2 from high to low (p2) + !phi2
# - iclk_delay, ~phi2 but with the start delayed to be after the end of iclk_pulse (p3)
#
# We represent that as three phases

class Timer1(Elaboratable):
    def __init__(self):
        self.i_clkp1 = Signal()
        self.i_clkp2 = Signal()
        self.i_clkp3 = Signal()

        self.i_d = Signal(8)
        self.i_t1ll_r = Signal()
        self.i_t1ll_w = Signal()
        self.i_t1cl_r = Signal()
        self.i_t1lh_r = Signal()
        self.i_t1lh_w = Signal()
        self.i_t1ch_r = Signal()

        self.o_d = Signal(8)
        
class Pa(Elaboratable):
    def __init__(self):
        self.i_rp = Signal(8)
        self.i_p = Signal(8)
        self.i_p_input_latch = Signal()

        self.o_rp = Signal(8)
        self.o_p = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o_p.eq(self.i_rp)
        with m.If(self.i_p_input_latch):
            m.d.comb += self.o_rp.eq(self.i_p)
        return m


class Ora(Elaboratable):
    def __init__(self):
        self.i_clkp1 = Signal()
        self.i_clkp2 = Signal()
        self.i_clkp3 = Signal()

        self.i_p = Signal(8)
        self.i_d = Signal(8)
        self.i_or_r = Signal()
        self.i_or_w = Signal()
        self.i_ddr_r = Signal()
        self.i_ddr_w = Signal()
        self.i_res = Signal()

        self.o_p = Signal(8)
        self.o_d = Signal(8)

        self.c_or = Signal(8)
        self.c_ddr = Signal(8)

    def elaborate(self, platform):
        m = Module()
        with m.If(~self.i_res):
            m.d.sync += self.c_or.eq(0x00)
        with m.Elif(self.i_or_w & self.i_clkp2):
            m.d.sync += self.c_or.eq(self.i_d)

        with m.If(~self.i_res):
            m.d.sync += self.c_ddr.eq(0x00)
        with m.Elif(self.i_ddr_w & self.i_clkp2):
            m.d.sync += self.c_ddr.eq(self.i_d)

        with m.If(self.i_clkp3):
            with m.If(self.i_or_r):
                m.d.sync += self.o_d.eq(self.i_p)
            with m.Elif(self.i_ddr_r):
                m.d.sync += self.o_d.eq(self.c_ddr)
            with m.Else():
                m.d.sync += self.o_d.eq(0xff)

        m.d.comb += self.o_p.eq(self.c_or | ~self.c_ddr)
        return m

# TODO: pb7 is different
class Pb(Elaboratable):
    def __init__(self):
        self.i_rp = Signal(8)
        self.i_rddr = Signal(8)
        self.i_p = Signal(8)
        self.i_p_input_latch = Signal()

        self.o_rp = Signal(8)
        self.o_ddr = Signal(8)
        self.o_p = Signal(8)

        self.c_p = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o_p.eq(self.i_rp)
        m.d.comb += self.o_ddr.eq(self.i_rddr)
        m.d.comb += self.o_rp.eq((self.i_rp & self.i_rddr) | (self.c_p & ~self.i_rddr))
        with m.If(self.i_p_input_latch):
            m.d.comb += self.c_p.eq(self.i_p)
        return m

class Orb(Elaboratable):
    def __init__(self):
        self.i_clkp1 = Signal()
        self.i_clkp2 = Signal()
        self.i_clkp3 = Signal()

        self.i_p = Signal(8)
        self.i_d = Signal(8)
        self.i_or_r = Signal()
        self.i_or_w = Signal()
        self.i_ddr_r = Signal()
        self.i_ddr_w = Signal()
        self.i_res = Signal()

        self.o_p = Signal(8)
        self.o_ddr = Signal(8)
        self.o_d = Signal(8)

        self.c_or = Signal(8)
        self.c_ddr = Signal(8)

    def elaborate(self, platform):
        m = Module()
        with m.If(~self.i_res):
            m.d.sync += self.c_or.eq(0x00)
        with m.Elif(self.i_or_w & self.i_clkp2):
            m.d.sync += self.c_or.eq(self.i_d)

        with m.If(~self.i_res):
            m.d.sync += self.c_ddr.eq(0x00)
        with m.Elif(self.i_ddr_w & self.i_clkp2):
            m.d.sync += self.c_ddr.eq(self.i_d)

        with m.If(self.i_clkp3):
            with m.If(self.i_or_r):
                m.d.sync += self.o_d.eq(self.i_p)
            with m.Elif(self.i_ddr_r):
                m.d.sync += self.o_d.eq(self.c_ddr)
            with m.Else():
                m.d.sync += self.o_d.eq(0xff)

        m.d.comb += self.o_p.eq(self.c_or)
        m.d.comb += self.o_ddr.eq(self.c_ddr)
        return m

class Reg(Elaboratable):
    def __init__(self):
        self.i_clkp1 = Signal()
        self.i_clkp2 = Signal()
        self.i_clkp3 = Signal()

        self.o_d = Signal(8)
        self.i_d = Signal(8)
        self.i_r = Signal()
        self.i_w = Signal()
        self.i_res = Signal()
        self.c_reg = Signal(8)

    def elaborate(self, platform):
        m = Module()
        with m.If(~self.i_res):
            m.d.sync += self.c_reg.eq(0x00)
        with m.Elif(self.i_w & self.i_clkp2):
            m.d.sync += self.c_reg.eq(self.i_d)

        with m.If(self.i_clkp3):
            with m.If(self.i_r):
                m.d.sync += self.o_d.eq(self.c_reg)
            with m.Else():
                m.d.sync += self.o_d.eq(0xff)
        return m

class via6522(Elaboratable):
    def __init__(self):
        self.i_clkp1 = Signal()
        self.i_clkp2 = Signal()
        self.i_clkp3 = Signal()

        self.o_d = Signal(8)
        self.i_d = Signal(8)
        self.o_d_drive = Signal()
        self.i_rs = Signal(4)
        self.i_cs1 = Signal()
        self.i_cs2 = Signal()
        self.i_rw = Signal()
        self.o_irq = Signal()
        self.i_ca1 = Signal()
        self.o_ca1 = Signal()
        self.o_ca1_drive = Signal()
        self.i_ca2 = Signal()
        self.o_ca2 = Signal()
        self.o_ca2_drive = Signal()
        self.i_cb1 = Signal()
        self.o_cb1 = Signal()
        self.o_cb1_drive = Signal()
        self.i_cb2 = Signal()
        self.o_cb2 = Signal()
        self.o_cb2_drive = Signal()
        self.i_pa = Signal(8)
        self.o_pa = Signal(8)
        self.i_pb = Signal(8)
        self.o_pb = Signal(8)
        self.o_pb_drive = Signal(8)
        self.i_res = Signal()

        self.o_ddrx = Signal(8)
        self.o_dw   = Signal()

        self.c_cs  = Signal()
        self.c_rw  = Signal()
        self.c_r   = Signal()
        self.c_w   = Signal()
        self.c_rs  = Signal(4)
        self.c_rsl = Signal(4)
        self.c_d   = Signal(8)
    def elaborate(self, platform):
        m = Module()
        m.submodules.ora = ora = Ora()
        m.submodules.pa  = pa  = Pa()
        m.submodules.orb = orb = Orb()
        m.submodules.pb  = pb  = Pb()
        m.submodules.pcr = pcr = Reg()
        m.submodules.acr = acr = Reg()

        m.d.comb += self.o_ddrx.eq(orb.c_ddr)
        m.d.comb += self.o_dw.eq(orb.i_ddr_w)
        
        # connect the clocks
        m.d.comb += ora.i_clkp1.eq(self.i_clkp1)
        m.d.comb += ora.i_clkp2.eq(self.i_clkp2)
        m.d.comb += ora.i_clkp3.eq(self.i_clkp3)
        m.d.comb += orb.i_clkp1.eq(self.i_clkp1)
        m.d.comb += orb.i_clkp2.eq(self.i_clkp2)
        m.d.comb += orb.i_clkp3.eq(self.i_clkp3)
        m.d.comb += pcr.i_clkp1.eq(self.i_clkp1)
        m.d.comb += pcr.i_clkp2.eq(self.i_clkp2)
        m.d.comb += pcr.i_clkp3.eq(self.i_clkp3)
        m.d.comb += acr.i_clkp1.eq(self.i_clkp1)
        m.d.comb += acr.i_clkp2.eq(self.i_clkp2)
        m.d.comb += acr.i_clkp3.eq(self.i_clkp3)

        # connect the buses
        m.d.comb += self.o_d.eq(ora.o_d & orb.o_d & pcr.o_d & acr.o_d)

        m.d.comb += ora.i_d.eq(self.c_d)
        m.d.comb += ora.i_p.eq(pa.o_rp)
        m.d.comb += pa.i_rp.eq(ora.o_p)
        m.d.comb += self.o_pa.eq(pa.o_p)
        m.d.comb += pa.i_p.eq(self.i_pa)
        m.d.comb += ora.i_res.eq(self.i_res)

        m.d.comb += orb.i_d.eq(self.c_d)
        m.d.comb += orb.i_p.eq(pb.o_rp)
        m.d.comb += pb.i_rp.eq(orb.o_p)
        m.d.comb += pb.i_rddr.eq(orb.o_ddr)
        m.d.comb += self.o_pb.eq(pb.o_p)
        m.d.comb += self.o_pb_drive.eq(pb.o_ddr)
        m.d.comb += pb.i_p.eq(self.i_pb)
        m.d.comb += orb.i_res.eq(self.i_res)

        m.d.comb += pcr.i_d.eq(self.c_d)
        m.d.comb += pcr.i_res.eq(self.i_res)

        m.d.comb += acr.i_d.eq(self.c_d)
        m.d.comb += acr.i_res.eq(self.i_res)
        
        # chip select and r/w handling, clocked on p3
        with m.If(self.i_clkp3):
            m.d.sync += self.c_cs.eq(self.i_cs1 & ~self.i_cs2)
            m.d.sync += self.c_rw.eq(self.i_rw)

        m.d.comb += self.c_r.eq(self.c_cs & self.c_rw)
        m.d.comb += self.c_w.eq(self.c_cs & ~self.c_rw)
        
        # data i/o
        with m.If(self.i_clkp1):
            m.d.sync += self.o_d_drive.eq(self.c_cs & self.c_rw & ~self.i_res)
        with m.If(self.i_clkp1):
            m.d.sync += self.c_d.eq(self.i_d)

        # rs latching and address decode
        with m.If(self.i_clkp3):
            m.d.sync += self.c_rs.eq(self.i_rs)
        with m.If(self.i_clkp1):
            m.d.sync += self.c_rsl.eq(self.c_rs)
        
        m.d.comb += ora.i_or_r.eq(self.c_r & ((self.c_rs  == 0xf) | (self.c_rs  == 0x1)))
        m.d.comb += ora.i_or_w.eq(self.c_w & ((self.c_rsl == 0xf) | (self.c_rsl == 0x1)))
        m.d.comb += ora.i_ddr_r.eq(self.c_r & (self.c_rs  == 0x3))
        m.d.comb += ora.i_ddr_w.eq(self.c_w & (self.c_rsl == 0x3))

        m.d.comb += orb.i_or_r.eq(self.c_r & (self.c_rs  == 0x0))
        m.d.comb += orb.i_or_w.eq(self.c_w & (self.c_rsl == 0x0))
        m.d.comb += orb.i_ddr_r.eq(self.c_r & (self.c_rs  == 0x2))
        m.d.comb += orb.i_ddr_w.eq(self.c_w & (self.c_rsl == 0x2))

        m.d.comb += pcr.i_r.eq(self.c_r & (self.c_rs  == 0xc))
        m.d.comb += pcr.i_w.eq(self.c_w & (self.c_rsl == 0xc))
        m.d.comb += acr.i_r.eq(self.c_r & (self.c_rs  == 0xb))
        m.d.comb += acr.i_w.eq(self.c_w & (self.c_rsl == 0xb))

        m.d.comb += pa.i_p_input_latch.eq(1)
        m.d.comb += pb.i_p_input_latch.eq(1)
        return m
