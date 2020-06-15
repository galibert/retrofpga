#define CXXRTL_INCLUDE_VCD_CAPI_IMPL

#include "m68000.cc"

using namespace cxxrtl;

cxxrtl_design::p_m68000 m68000;
debug_items ditems;
const debug_item *clk, *pclk, *nclk;

const debug_item *o_e;

void stepp()
{
  pclk->next[0] = 1;
  clk->next[0] = 0;
  m68000.step();
  clk->next[0] = 1;
  m68000.step();
  pclk->next[0] = 0;
}

void stepn()
{
  nclk->next[0] = 1;
  clk->next[0] = 0;
  m68000.step();
  clk->next[0] = 1;
  m68000.step();
  nclk->next[0] = 0;
}

void reset()
{
  auto &res = ditems["rst"];
  res.next[0] = 1;
  stepp();
  stepn();
  res.next[0] = 0;
}

int main(int argc, char **argv)
{
  m68000.debug_info(ditems, "");

  clk = &ditems["clk"];
  pclk = &ditems["i_pclk"];
  nclk = &ditems["i_nclk"];
  o_e  = &ditems["o_e"];

  auto &state = ditems["eclock estate"];
  auto &lfsr = ditems["eclock elfsr"];
  auto &nlfsr = ditems["eclock enlfsr"];
  auto &ereset = ditems["eclock ereset"];

  reset();

  for(int i=0; i != 60; i++) {
    printf("%3d: %d (%x %x) -> %x reset=%x\n", i, o_e->curr[0], lfsr.curr[0], nlfsr.curr[0], state.curr[0], ereset.curr[0]);
    if(i & 1)
      stepn();
    else
      stepp();
  }
  return 0;
}
