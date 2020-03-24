from via6522 import via6522
from nmigen import *
from nmigen.back.pysim import *

base_clock = 0.5/3/1e-6
via = via6522()

sim = Simulator(via)

sim.add_clock(base_clock, phase=0, domain="sync")

def clocking_proc():
    while True:
        yield via.i_clkp1.eq(1)
        yield via.i_clkp2.eq(0)
        yield via.i_clkp3.eq(0)
        yield Tick()
        yield via.i_clkp1.eq(0)
        yield via.i_clkp2.eq(1)
        yield via.i_clkp3.eq(0)
        yield Tick()
        yield via.i_clkp1.eq(0)
        yield via.i_clkp2.eq(0)
        yield via.i_clkp3.eq(1)
        yield Tick()

sim.add_process(clocking_proc)

def stimulus_proc():
    def w(a, d):
        while (yield via.i_clkp3) == 0:
            yield Tick()
        yield via.i_cs1.eq(1)
        yield via.i_cs2.eq(0)
        yield via.i_rw.eq(0)
        yield via.i_rs.eq(a)
        yield Tick()
        yield via.i_d.eq(d)        
        while (yield via.i_clkp3) == 0:
            yield Tick()
        yield via.i_cs1.eq(0)
        yield via.i_cs2.eq(1)
    
    # Start by resetting
    yield via.i_res.eq(0)
    yield via.i_rs.eq(0x0)
    yield via.i_pa.eq(0xff)
    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)
    yield via.i_rw.eq(1)
    for i in range(0, 10):
        yield Tick()
    yield via.i_res.eq(1)
    for i in range(0, 10):
        yield Tick()

    # Write ddra to all output
    yield from w(0x2, 0xff)

    # Write some values in ora
    for i in range(0, 16):
        yield from w(0, i*0x11)

    yield via.i_cs1.eq(0)
    yield via.i_cs2.eq(1)

sim.add_process(stimulus_proc)

with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run_until(300*base_clock)
