from k053252 import k053252
from nmigen import *
from nmigen.back.pysim import *

# Base clock is 12MHz or 16MHz
base_clock = 1/(12e6)

ccu = k053252()
sim = Simulator(ccu)

sim.add_clock(base_clock, phase=0, domain="sync")

def stimulus_proc():
    yield ccu.i_ccs.eq(1)
    yield ccu.i_clkp.eq(1)
    while True:
        yield Tick()


sim.add_process(stimulus_proc)

with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run_until(3/60)
