import sys
sys.path.append('..')

from k053252 import k053252
from k051316 import k051316
from nmigen import *
from nmigen.back import rtlil
from nmigen.back.pysim import *

def rom_load_bytes(fname):
    rawdata = open(fname, 'rb').read()
    r = []
    for i in range(0, len(rawdata)):
        r.append(rawdata[i])
    return r

class overdrive(Elaboratable):
    def __init__(self):
        self.o_nhsy = Signal()
        self.o_nhbk = Signal()
        self.o_nvsy = Signal()
        self.o_nvbk = Signal()

        self.o_ci3 = Signal(8)
        self.o_ci4 = Signal(8)

        self.o_ca  = Signal(24)
        self.o_xcp = Signal(24)
        self.o_ycp = Signal(24)
        self.o_vramadr = Signal(10)

        self.m_timings = k053252.k053252()
        self.m_roz_1   = k051316.k051316('captures/first_1_roz_1.bin', [ 0, 0x800, 0, 0, 0, 0x800, 0, 7 ])
        self.m_roz_2   = k051316.k051316('captures/first_1_roz_2.bin', [ 0x400b, 0, 0xf6, -0x5602, -0x1f7, 0, 0, 3 ])

        roz1r = rom_load_bytes("roms/789e06.a21")
        self.roz1_rom = Memory(width = 8, depth = 0x20000, init = roz1r)

        roz2r = rom_load_bytes("roms/789e07.c23")
        self.roz2_rom = Memory(width = 8, depth = 0x20000, init = roz2r)

        

    def elaborate(self, platform):
        m = Module()
        m.submodules += self.m_timings
        m.submodules += self.m_roz_1
        m.submodules += self.m_roz_2
        roz1rd = self.roz1_rom.read_port()
        roz2rd = self.roz2_rom.read_port()
        m.submodules += [roz1rd, roz2rd]

        m.d.comb += self.o_nhsy.eq(self.m_timings.o_nhsy)
        m.d.comb += self.o_nvsy.eq(self.m_timings.o_nvsy)
        m.d.comb += self.o_nhbk.eq(self.m_timings.o_nhbk)
        m.d.comb += self.o_nvbk.eq(self.m_timings.o_nvbk)

        m.d.comb += self.m_roz_1.i_clk2.eq(self.m_timings.o_clk2)
        m.d.comb += self.m_roz_1.i_nhsy.eq(self.m_timings.o_nhsy)
        m.d.comb += self.m_roz_1.i_nhbk.eq(self.m_timings.o_nhbk)
        m.d.comb += self.m_roz_1.i_nvsy.eq(self.m_timings.o_nvsy)
        m.d.comb += self.m_roz_1.i_nvbk.eq(self.m_timings.o_nvbk)
        m.d.comb += roz1rd.addr.eq(self.m_roz_1.o_ca[1:18])
        with m.If(self.m_roz_1.o_ca[0]):
            m.d.comb += self.o_ci4[:4].eq(roz1rd.data[4:])
        with m.Else():
            m.d.comb += self.o_ci4[:4].eq(roz1rd.data[:4])
        m.d.comb += self.o_ci4[4:].eq(self.m_roz_1.o_ca[18:22])

        m.d.comb += self.o_ca.eq(self.m_roz_1.o_ca)
        m.d.comb += self.o_xcp.eq(self.m_roz_1.o_xcp)
        m.d.comb += self.o_ycp.eq(self.m_roz_1.o_ycp)
        m.d.comb += self.o_vramadr.eq(self.m_roz_1.o_vramadr)

        m.d.comb += self.m_roz_2.i_clk2.eq(self.m_timings.o_clk2)
        m.d.comb += self.m_roz_2.i_nhsy.eq(self.m_timings.o_nhsy)
        m.d.comb += self.m_roz_2.i_nhbk.eq(self.m_timings.o_nhbk)
        m.d.comb += self.m_roz_2.i_nvsy.eq(self.m_timings.o_nvsy)
        m.d.comb += self.m_roz_2.i_nvbk.eq(self.m_timings.o_nvbk)
        m.d.comb += roz2rd.addr.eq(self.m_roz_2.o_ca[1:18])
        with m.If(self.m_roz_2.o_ca[0]):
            m.d.comb += self.o_ci3[:4].eq(roz2rd.data[4:])
        with m.Else():
            m.d.comb += self.o_ci3[:4].eq(roz2rd.data[:4])
        m.d.comb += self.o_ci3[4:].eq(self.m_roz_2.o_ca[18:22])

        m.d.comb += self.m_timings.i_ccs.eq(1)
        m.d.comb += self.m_timings.i_ab.eq(0)
        m.d.comb += self.m_timings.i_db.eq(0)
        m.d.comb += self.m_timings.i_rw.eq(1)

        m.d.comb += self.m_roz_1.i_iocs.eq(1)
        m.d.comb += self.m_roz_1.i_vrcs.eq(1)
        m.d.comb += self.m_roz_1.i_ab.eq(0)
        m.d.comb += self.m_roz_1.i_db.eq(0)
        m.d.comb += self.m_roz_1.i_rw.eq(1)

        m.d.comb += self.m_roz_2.i_iocs.eq(1)
        m.d.comb += self.m_roz_2.i_vrcs.eq(1)
        m.d.comb += self.m_roz_2.i_ab.eq(0)
        m.d.comb += self.m_roz_2.i_db.eq(0)
        m.d.comb += self.m_roz_2.i_rw.eq(1)
        return m


if True:
    rtlil_text = rtlil.convert(overdrive(), platform=None, name="overdrive")
    print("""
    read_ilang <<rtlil
    {}
    rtlil
    proc
    flatten
    memory_collect
    expose w:o_* w:*$next %d
    opt -full
    clean -purge
    write_cxxrtl
    """.format(rtlil_text))
else:
    over = overdrive()
    sim = Simulator(over)

    sim.add_clock(1/(12e6), phase=0, domain="sync")

    def stimulus_proc():
        while True:
            yield Tick()

    sim.add_process(stimulus_proc)
    with sim.write_vcd("test.vcd", "test.gtkw"):
        sim.run_until(3/60)

