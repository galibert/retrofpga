from wd1772 import wd1772
from nmigen import *
from nmigen.back.pysim import *

base_clock = 0.5/8e6
wd = wd1772()
sim = Simulator(wd)

sim.add_clock(base_clock, phase=0, domain="sync")

def clocking_proc():
    while True:
        yield wd.i_clkp.eq(1)
        yield wd.i_clkn.eq(0)
        yield Tick()
        yield wd.i_clkp.eq(0)
        yield wd.i_clkn.eq(1)
        yield Tick()

sim.add_process(clocking_proc)

def signals_proc():
    yield wd.i_mr.eq(0)
    yield wd.i_rd.eq(1)
    for i in range(8):
        yield Tick()
    yield wd.i_mr.eq(1)
    yield Tick()
    
sim.add_process(signals_proc)

with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run_until(1000*base_clock)
