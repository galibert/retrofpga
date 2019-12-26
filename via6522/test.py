from via6522 import via6522
from nmigen import *
from nmigen.back.pysim import *

base_clock = 10e-9 # To make things easier under gtkwave
via = via6522()
ports = [ via.i_d, via.i_pa, via.i_rs, via.i_cs1, via.i_cs2, via.i_rw, via.i_res, via.o_d, via.o_pa ]

sim = Simulator(via)

def clocking_proc(period=base_clock):
    yield Delay(period)
    while True:
        yield via.ck0p.clk.eq(1)
        yield via.ck0n.clk.eq(0)
        yield Delay(period/2)
        yield via.ck0p.clk.eq(0)
        yield via.ck0n.clk.eq(1)
        yield Delay(period/2)
sim.add_process(clocking_proc)

def wr(reg, value):
    yield via.i_cs1.eq(1)
    yield via.i_cs2.eq(0)
    yield via.i_rw.eq(0)
    yield via.i_rs.eq(reg)
    yield Tick("ck1p")
    yield via.i_d.eq(value)
    yield Tick("ck0p")
    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)

def rr(reg, value):
    yield via.i_cs1.eq(1)
    yield via.i_cs2.eq(0)
    yield via.i_rw.eq(1)
    yield via.i_rs.eq(reg)
    yield Tick("ck1p")
    yield Tick("ck0p")
    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)
        
def stimulus_proc():
    # Start by resetting
    yield via.i_res.eq(0)
    yield via.i_rs.eq(0x0)
    yield via.i_pa.eq(0xff)
    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)
    yield via.i_rw.eq(1)
    for i in range(0, 2):
        yield Tick("ck0p")
    yield via.i_res.eq(1)

    # Write ddra to all output
    wr(0x3, 0xff)

    # Scan all possible values in ora
    for i in range(0, 256):
        wr(0x1, i)

sim.add_process(stimulus_proc)

with sim.write_vcd("test.vcd", "test.gtkw", traces=ports):
    sim.run_until(260*base_clock)
