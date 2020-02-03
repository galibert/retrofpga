#include <stdio.h>
#include "overdrive.cc"

int main()
{
  cxxrtl_design::p_overdrive overdrive;

  overdrive.p_i__ccs.next = value<1>{1u};
  overdrive.step();

  int prev = 0x1010;

  for (unsigned i = 0; i < 100*384*264; i++) {
    int next =
      (overdrive.p_o__nvsy.curr.data[0] << 12) |
      (overdrive.p_o__nvbk.curr.data[0] << 8) |
      (overdrive.p_o__nhsy.curr.data[0] << 4) |
      overdrive.p_o__nhbk.curr.data[0];

    if(next != prev) {
      if((prev & 0x100) && !(next & 0x100))
	fprintf(stderr, "%6d: vblank start\n", i);
      fprintf(stderr, "%04x\n", next);
      prev = next;
    }

    // more compatible but slightly slower code: explicitly drive a clock signal
    // overdrive.p_clk.next = value<1>{1u};
    // overdrive.step();
    // overdrive.p_clk.next = value<1>{0u};
    // overdrive.step();
    // less compatible but slightly faster code: trigger events directly
    // overdrive.posedge_p_clk = true;
    // overdrive.step();
    // even less compatible but even faster code: omit delta cycles
    overdrive.posedge_p_clk = true;
    overdrive.eval();
    overdrive.commit();
  }
}
