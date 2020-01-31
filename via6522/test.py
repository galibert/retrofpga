from via6522 import via6522
from nmigen import *
from nmigen.back.pysim import *

base_clock = 1e-6 # To make things easier under gtkwave
via = via6522()

sim = Simulator(via)

sim.add_clock(base_clock, phase=0, domain="ck0p")
sim.add_clock(base_clock, phase=base_clock/2, domain="ck0n")

#sim.add_inputs([via.i_cs1, via.i_cs2, via.i_rw, via.i_rs, via.i_d, via.m_ora.c_ddr])

def stimulus_proc():
    # Start by resetting
    yield via.i_res.eq(0)
    yield via.i_rs.eq(0x0)
    yield via.i_pa.eq(0xff)
    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)
    yield via.i_rw.eq(1)
    for i in range(0, 2):
        yield Tick(via.ck0p)
    yield Delay(base_clock/4)
    yield via.i_res.eq(1)
    for i in range(0, 2):
        yield Tick(via.ck0p)

    yield Tick(via.ck0n)
    yield Delay(base_clock/4)

    # Write ddra to all output
    yield via.i_cs1.eq(1)
    yield via.i_cs2.eq(0)
    yield via.i_rw.eq(0)
    yield via.i_rs.eq(0x2)
    yield Tick(via.ck0p)
    yield Delay(base_clock/4)
    yield via.i_d.eq(0xff)
    yield Tick(via.ck0n)
    yield Delay(base_clock/4)

    # Write some values in ora
    for i in range(0, 16):
        yield via.i_cs1.eq(1)
        yield via.i_cs2.eq(0)
        yield via.i_rw.eq(0)
        yield via.i_rs.eq(0x0)
        yield Tick(via.ck0p)
        yield Delay(base_clock/4)
        yield via.i_d.eq(i*0x11)
        yield Tick(via.ck0n)
        yield Delay(base_clock/4)

    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)
    yield Delay(10*base_clock)

sim.add_process(stimulus_proc)

with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run_until(100*base_clock)
