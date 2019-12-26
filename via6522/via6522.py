from nmigen import *

# Chip has one clock, phi2.  Three clocks signals are generated from it
# - phi2 itself
# - iclk_pulse, a small length pulse on transition on phi2 from high to low
# - iclk_delay, ~phi2 but with the start delayed to be after the end of iclk_pulse
#
# Given it's nmos:
# - keying on phi2 means the signal is available to read on negative pulse -> trigger on ck0p
# - keying on iclk_delay means the signal is available to read on positive pulse -> trigger on ck0n
# - keying on pulse means a signal is read on negative pulse -> trigger on ck0n

class pa(Elaboratable):
    def __init__(self):
        self.i_rp = Signal(8)
        self.o_rp = Signal(8)
        self.i_p = Signal(8)
        self.o_p = Signal(8)
        self.i_p_input_latch = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o_p.eq(self.i_rp)
        with m.If(self.i_p_input_latch):
            m.d.comb += self.o_rp.eq(self.i_p)
        return m


class ora(Elaboratable):
    def __init__(self):
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
            m.d.ck0n += self.c_or.eq(0x00)
        with m.Elif(self.i_or_w):
            m.d.ck0n += self.c_or.eq(self.i_d)

        with m.If(~self.i_res):
            m.d.ck0n += self.c_ddr.eq(0x00)
        with m.Elif(self.i_ddr_w):
            m.d.ck0n += self.c_ddr.eq(self.i_d)

        with m.If(self.i_or_r):
            m.d.ck0p += self.o_d.eq(self.i_p)
        with m.Elif(self.i_ddr_r):
            m.d.ck0p += self.o_d.eq(self.c_ddr)
        with m.Else():
            m.d.ck0p += self.o_d.eq(0xff)

        m.d.comb += self.o_p.eq(self.c_or | ~self.c_ddr)
        return m


class via6522(Elaboratable):
    def __init__(self):
        self.ck0p = ClockDomain()
        self.ck0n = ClockDomain()
        self.o_d = Signal(8)
        self.i_d = Signal(8)
        self.o_d_drive = Signal() # valid on 
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
        self.i_pb_drive = Signal(8)
        self.i_res = Signal()

        self.c_cs = Signal()
        self.c_rw = Signal()
        self.c_r = Signal()
        self.c_w = Signal()
        self.c_rs = Signal(4)

        self.m_ora = ora()
        self.m_pa = pa()

    def elaborate(self, platform):
        m = Module()
        m.domains += self.ck0p, self.ck0n
        m.submodules += self.m_ora
        m.submodules += self.m_pa

        # connect the buses
        m.d.comb += self.m_ora.i_d.eq(self.i_d)
        m.d.comb += self.o_d.eq(self.m_ora.o_d & 0xff)
        m.d.comb += self.m_ora.i_p.eq(self.m_pa.o_rp)
        m.d.comb += self.m_pa.i_rp.eq(self.m_ora.o_p)
        m.d.comb += self.o_pa.eq(self.m_pa.o_p)
        m.d.comb += self.m_pa.i_p.eq(self.i_pa)
        m.d.comb += self.m_ora.i_res.eq(self.i_res)

        # chip select and r/w handling
        m.d.comb += self.c_cs.eq(self.i_cs1 & ~self.i_cs2)
        m.d.comb += self.c_rw.eq(self.i_rw)
        m.d.comb += self.c_r.eq(self.c_cs & self.c_rw)
        m.d.comb += self.c_w.eq(self.c_cs & ~self.c_rw)
        
        # data i/o
        m.d.ck0p += self.o_d_drive.eq(self.c_cs & self.c_rw & ~self.i_res)

        # rs latching and address decode
        m.d.ck0p += self.c_rs.eq(self.i_rs)
        
        m.d.comb += self.m_ora.i_or_r.eq(self.c_r & ((self.i_rs == 0xf) | (self.i_rs == 0x1)))
        m.d.comb += self.m_ora.i_or_w.eq(self.c_w & ((self.c_rs == 0xf) | (self.c_rs == 0x1)))
        m.d.comb += self.m_ora.i_ddr_r.eq(self.c_r & (self.i_rs == 0x3))
        m.d.comb += self.m_ora.i_ddr_w.eq(self.c_w & (self.c_rs == 0x3))

        m.d.comb += self.m_pa.i_p_input_latch.eq(1)
        return m
