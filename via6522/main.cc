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

void cycle()
{
  W(p_i__clkp1, 1, 1u);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  W(p_i__clkp1, 1, 0u);
  W(p_i__clkp2, 1, 1u);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  W(p_i__clkp2, 1, 0u);
  W(p_i__clkp3, 1, 1u);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  W(p_i__clkp3, 1, 0u);
}

void w(u8 adr, u8 data)
{
  W(p_i__cs1, 1, 1U);
  W(p_i__cs2, 1, 0U);
  W(p_i__rs, 4, adr);
  W(p_i__rw, 1, 0U);

  W(p_i__clkp1, 1, 1u);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  //  printf("a == a=%x d=%02x w=%d (%02x %d)\n", R(p_i__rs), R(p_i__d), R(p_o__dw), R(p_o__ddrx), R(p_o__dw));
  W(p_i__clkp1, 1, 0u);
  W(p_i__clkp2, 1, 1u);
  W(p_i__d, 8, data);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  //  printf("b == a=%x d=%02x w=%d (%02x %d)\n", R(p_i__rs), R(p_i__d), R(p_o__dw), R(p_o__ddrx), R(p_o__dw));
  W(p_i__clkp2, 1, 0u);
  W(p_i__clkp3, 1, 1u);
  W(p_clk, 1, 1u);
  via6522.step();
  W(p_clk, 1, 0u);
  via6522.step();
  //  printf("c == a=%x d=%02x w=%d (%02x %d)\n", R(p_i__rs), R(p_i__d), R(p_o__dw), R(p_o__ddrx), R(p_o__dw));
  W(p_i__clkp3, 1, 0u);
  W(p_i__cs1, 1, 0U);
  W(p_i__cs2, 1, 1U);
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

  printf(".. -> pa=%02x pb=%02x.%02x (%02x %d)\n", R(p_o__pa), R(p_o__pb), R(p_o__pb__drive), R(p_o__ddrx), R(p_o__dw));
  w(0x3, 0xf8);
  printf(".. -> pa=%02x pb=%02x.%02x (%02x %d)\n", R(p_o__pa), R(p_o__pb), R(p_o__pb__drive), R(p_o__ddrx), R(p_o__dw));
  for(int i=0; i<16; i++) {
    w(0x1, i*0x11);
    printf("%02x -> pa=%02x pb=%02x.%02x (%02x %d)\n", i, R(p_o__pa), R(p_o__pb), R(p_o__pb__drive), R(p_o__ddrx), R(p_o__dw));
  }
}


int main(int argc, char **argv)
{
  run_design();

  return 0;
}
