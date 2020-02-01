from k053252 import k053252
from nmigen import *
from nmigen.back.pysim import *

# Base clock is 6, 8 or 12MHz
base_clock = 1/(6e6)

ccu = k053252()
sim = Simulator(ccu)

sim.add_clock(base_clock, phase=0, domain="sync")

def stimulus_proc():
    yield ccu.i_ccs.eq(1)
    while True:
        yield Tick()


sim.add_process(stimulus_proc)

with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run_until(3/60)
