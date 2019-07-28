from wd1772 import wd1772
from nmigen import *
from nmigen.back.pysim import *

base_clock = 10e-9 # To make things easier under gtkwave, 125e-9 in reality
wd = wd1772()
ports = [ wd.i_adr, wd.o_rom ]
with Simulator(wd,
               vcd_file=open("test.vcd", "w"),
               gtkw_file=open("test.gtkw", "w"),
               traces=ports) as sim:

    def clocking_proc(period=base_clock):
        yield Delay(period)
        while True:
            yield wd.ck0p.clk.eq(1)
            yield wd.ck0n.clk.eq(0)
            yield Delay(period/2)
            yield wd.ck0p.clk.eq(0)
            yield wd.ck0n.clk.eq(1)
            yield Delay(period/2)
    sim.add_process(clocking_proc())

    def stimulus_proc():
        for i in range(0, 256):
            yield Tick("ck0p")
            yield wd.i_adr.eq(i)
    sim.add_process(stimulus_proc())
    sim.run_until(260*base_clock)
