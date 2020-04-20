#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "via6522.cc"

typedef   signed char  s8;
typedef unsigned char  u8;
typedef   signed short s16;
typedef unsigned short u16;
typedef   signed int   s32;
typedef unsigned int   u32;
typedef   signed long  s64;
typedef unsigned long  u64;

cxxrtl_design::p_via6522 via6522;

#define R(port) (via6522.port.curr.data[0])
#define W(port, bits, val) via6522.port.next = value<bits>(val)

void step(int phase)
{
  W(p_i__clkp1, 1, 0u);
  W(p_i__clkp2, 1, 0u);
  W(p_i__clkp3, 1, 0u);
  switch(phase) {
  case 1: W(p_i__clkp1, 1, 1u); break;
  case 2: W(p_i__clkp2, 1, 1u); break;
  case 3: W(p_i__clkp3, 1, 1u); break;
  }

  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();

  switch(phase) {
  case 1: W(p_i__clkp1, 1, 0u); break;
  case 2: W(p_i__clkp2, 1, 0u); break;
  case 3: W(p_i__clkp3, 1, 0u); break;
  }
}

void cycle()
{
  step(2);
  step(3);
  step(1);
}

void w(u8 adr, u8 data)
{
  W(p_i__cs1, 1, 1U);
  W(p_i__cs2, 1, 0U);
  W(p_i__rs, 4, adr);
  W(p_i__rw, 1, 0U);

  step(3);
  step(1);

  W(p_i__d, 8, data);

  step(2);

  W(p_i__cs1, 1, 0U);
  W(p_i__cs2, 1, 1U);
}

u8 r(u8 adr)
{
  W(p_i__cs1, 1, 1U);
  W(p_i__cs2, 1, 0U);
  W(p_i__rs, 4, adr);
  W(p_i__rw, 1, 1U);

  step(3);
  step(1);

  u8 res = R(p_o__d);

  step(2);

  W(p_i__cs1, 1, 0U);
  W(p_i__cs2, 1, 1U);

  return res;
}

void reset()
{
  W(p_i__clkp1, 1, 0u);
  W(p_i__clkp2, 1, 0u);
  W(p_i__clkp3, 1, 0u);
  W(p_i__res, 1, 0u);
  W(p_i__cs1, 1, 0U);
  W(p_i__cs2, 1, 1U);
  W(p_i__rs, 4, 0U);
  W(p_i__rw, 1, 1U);
  W(p_i__pa, 8, 0xffU);

  cycle();
  cycle();
  W(p_i__res, 1, 1u);
  cycle();
  cycle();
}

void run_design()
{
  reset();

  w(0x2, 0xf7);
  w(0x0, 0xb7);
  w(0xc, 0xdd);
  w(0xe, 0x7f);
  w(0xb, 0x00);
  w(0xf, 0x07);
  cycle();
  cycle();
  printf("%02x / %02x\n", r(2), R(p_o__ddrx));
  cycle();
}


int main(int argc, char **argv)
{
  run_design();

  return 0;
}
