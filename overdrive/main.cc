#include <stdio.h>
#include <assert.h>
#include "overdrive.cc"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <zlib.h>

#include <functional>
#include <vector>

typedef   signed char  s8;
typedef unsigned char  u8;
typedef   signed short s16;
typedef unsigned short u16;
typedef   signed int   s32;
typedef unsigned int   u32;
typedef   signed long  s64;
typedef unsigned long  u64;

//   scores:
// roz 1: 0 8 0 0 0 8 0 7
// roz 2: 800d 0 f0 0 fe0f 0 0 3
// lvc 1: 0 b5 0 0 3b 0 0 0
// lvc 2: 0 57 0 0 62 0 0 0
// os  1: ffd3 feea 0 0 0
// os  2: 0 0 0 0 0 0 0 0 0 0 0 0 0 0
// 251:   [0 0 0 0 3e] [0 0] [0 0] 24 37 0 0 e
//    c0=0, c1=1, c2=2, c3=7, c4=6
//    l0 = obj  (9)
//    l1 = lvc1 (9)
//    l2 = lvc2 (9)
//    l3 = roz2 (8)
//    l4 = roz1 (8)

//   first 1:
// roz 1: 0 8 0 0 0 8 0 7
// roz 2: 400b 0 f6 a9fe fe09 0 0 3
// lvc 1: 0 b5 0 0 3b 0 0 0
// lvc 2: 0 57 0 0 62 0 0 0
// os  1: ff d3 fe ea 0 0 0 0
// os  2: 0
// 251  : [0 0 0 0 3e] [0 0] [0 0] 24 37 0 0 e

//#ifdef COMPAT
//    overdrive.p_clk.next = value<1>{1u};
//    overdrive.step();
//    overdrive.p_clk.next = value<1>{0u};
//    overdrive.step();
//#else
//    // even less compatible but even faster code: omit delta cycles
//    overdrive.posedge_p_clk = true;
//    overdrive.eval();
//    overdrive.commit();
//#endif
//    // less compatible but slightly faster code: trigger events directly
//    // overdrive.posedge_p_clk = true;
//    // overdrive.step();

struct rwrite {
  u32 adr;
  u16 data;
  u8 uds;
  u8 lds;
  u8 id;
};

u16 *palette;
u8 *roz_1_ram;
u8 *roz_2_ram;
u8 *lvc_ram;

std::vector<rwrite> rwrites;

constexpr int SX = 3*3;
constexpr int SY = (264*2+1)*9*3;
constexpr int SY1 = (264*2+1)*3*3;

unsigned char image[384*SY];

template<u32 nb> u32 inv(u32 v)
{
  u32 r = 0;
  for(u32 i=0; i != nb; i++)
    if(v & (1 << i))
      v |= 1 << (nb-1-i);
  return v;
}

static void w32(unsigned char *p, int l)
{
  p[0] = l>>24;
  p[1] = l>>16;
  p[2] = l>>8;
  p[3] = l;
}

static void wchunk(int fd, unsigned int type, unsigned char *p, unsigned int l)
{
  unsigned char v[8];
  unsigned int crc;
  w32(v, l);
  w32(v+4, type);
  write(fd, v, 8);
  crc = crc32(0, v+4, 4);
  if(l) {
    write(fd, p, l);
    crc = crc32(crc, p, l);
  }
  w32(v, crc);
  write(fd, v, 4);
}

void png_write(const char *name, const void *data, int width, int height)
{
  char msg[4096];
  sprintf(msg, "Error opening %s for writing", name);
  int fd = open(name, O_WRONLY|O_CREAT|O_TRUNC, 0666);
  if(fd<0) {
    perror(msg);
    exit(1);
  }

  const unsigned char *edata = (const unsigned char *)data;
  unsigned char *image = new unsigned char[(width*3+1)*height];
  unsigned char *ddata = image;

  for(int y=0; y<height; y++) {
    *ddata++ = 0;
    memcpy(ddata, edata, width*3);
    ddata += width*3;
    edata += width*3;
  }  

  unsigned long sz = (int)((width*3+1)*height*1.1+12);
  unsigned char *cdata = new unsigned char[sz];

  write(fd, "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", 8);

  w32(cdata, width);
  w32(cdata+4, height);
  cdata[8] = 8;
  cdata[9] = 2;
  cdata[10] = 0;
  cdata[11] = 0;
  cdata[12] = 0;
  wchunk(fd, 0x49484452L, cdata, 13); // IHDR

  compress(cdata, &sz, image, (width*3+1)*height);
  wchunk(fd, 0x49444154L, cdata, sz); // IDAT
  wchunk(fd, 0x49454E44L, 0, 0); // IEND
  close(fd);

  delete[] cdata;
  delete[] image;
}

void *file_load(const char *fname)
{
  char msg[4096];
  sprintf(msg, "Open %s", fname);
  int fd = open(fname, O_RDONLY);
  if(fd<0) {
    perror(msg);
    exit(2);
  }

  int size = lseek(fd, 0, SEEK_END);
  lseek(fd, 0, SEEK_SET);

  void *data = new unsigned char[size];
  read(fd, data, size);
  close(fd);

  return data;
}

cxxrtl_design::p_overdrive overdrive;

std::string tdelta(int duration)
{
  u64 v = u64(duration)*1000000000/24000000;
  char buf[4096];
  sprintf(buf, "%d.%03d_%03d_%03d",
	  int(v/1000000000),
	  int((v/1000000) % 1000),
	  int((v/1000) % 1000),
	  int(v % 1000));
  return buf;
}

int p24tick = 0;
int p12tick = 0;
int n12tick = 0;
int p6tick = 0;
int n6tick = 0;

#define R(port) (overdrive.port.curr.data[0])
#define W(port, bits, val) overdrive.port.next = value<bits>(val)

void rozshow(int x, int y)
{
  printf("%03d.%03d.%d%d%d%d.%d%d: col=%03x\n", x, y,
	 R(p_o__nvsy),
	 R(p_o__nvbk),
	 R(p_o__nhsy),
	 R(p_o__nhbk),
	 R(p_o__p6m),
	 R(p_o__n6m),
	 R(p_o__c0));
}


void show1(const char *mark = "")
{
  printf("%6d: 1 %c%c %c%c %c%c %c%c%c%c  as=%d%d%d a=%06x rw=%d dtack=%d datai=%04x datao=%04x %s\n",
	 p24tick,
	 R(p_o__p12m) ? '#' : '-',
	 R(p_o__n12m) ? '#' : '-',
	 R(p_o__p6m)  ? '#' : '-',
	 R(p_o__n6m)  ? '#' : '-',
	 R(p_o__p6md) ? '#' : '-',
	 R(p_o__n6md) ? '#' : '-',
	 R(p_o__nvbk) ? '-' : 'v',
	 R(p_o__nvsy) ? '-' : 'V',
	 R(p_o__nhbk) ? '-' : 'h',
	 R(p_o__nhsy) ? '-' : 'H',

	 R(p_i__as1),
	 R(p_i__uds1),
	 R(p_i__lds1),
	 R(p_i__ab1) << 1,
	 R(p_i__rw1),
	 R(p_o__dtack1),
	 R(p_i__db1),
	 R(p_o__db1),
	 mark);
}

void show2(const char *mark = "")
{
  printf("%6d: 2 %c%c %c%c %c%c %c%c%c%c  as=%d%d%d a=%06x rw=%d dtack=%d datai=%04x datao=%04x %s\n",
	 p24tick,
	 R(p_o__p12m) ? '#' : '-',
	 R(p_o__n12m) ? '#' : '-',
	 R(p_o__p6m)  ? '#' : '-',
	 R(p_o__n6m)  ? '#' : '-',
	 R(p_o__p6md) ? '#' : '-',
	 R(p_o__n6md) ? '#' : '-',
	 R(p_o__nvbk) ? '-' : 'v',
	 R(p_o__nvsy) ? '-' : 'V',
	 R(p_o__nhbk) ? '-' : 'h',
	 R(p_o__nhsy) ? '-' : 'H',

	 R(p_i__as2),
	 R(p_i__uds2),
	 R(p_i__lds2),
	 R(p_i__ab2) << 1,
	 R(p_i__rw2),
	 R(p_o__dtack2),
	 R(p_i__db2),
	 R(p_o__db2),
	 mark);
}

void reset()
{
  W(p_clk, 1, 1u);
  W(p_rst, 1, 1u);
  overdrive.step();
  W(p_clk, 1, 0u);
  overdrive.step();
  W(p_clk, 1, 1u);
  overdrive.step();
  W(p_clk, 1, 0u);
  W(p_rst, 1, 0u);
  overdrive.step();
}

void tick()
{
  W(p_clk, 1, 1u);
  overdrive.step();
  W(p_clk, 1, 0u);
  overdrive.step();

  p24tick ++;
  if(R(p_o__p12m))
    p12tick++;
  if(R(p_o__p12m))
    n12tick++;
  if(R(p_o__p6m))
    p6tick++;
  if(R(p_o__n6m))
    n6tick++;
}

void wait_p12m()
{
  do
    tick();
  while(!R(p_o__p12m));
}

void wait_n12m()
{
  do
    tick();
  while(!R(p_o__n12m));
}

void wait_p6m()
{
  do {
    tick();
  } while(!R(p_o__p6m));
}

void wait_n6m()
{
  do
    tick();
  while(!R(p_o__n6m));
}

void wait_p6md()
{
  do
    tick();
  while(!R(p_o__p6md));
}

void wait_n6md()
{
  do
    tick();
  while(!R(p_o__n6md));
}

void wait_until(std::function<bool ()> cb)
{
  do
    tick();
  while(!cb());
}

void m68000_1_w(std::function<void ()> wp, std::function<void ()> wn, u32 adr, u16 val, u8 uds, u8 lds, bool v = false)
{
  if(v)
    printf("Write cycle started %06x %04x %d%d\n", adr, val, uds, lds);
  wp(); // s0
  if(v)
    show1("s0");
  wn(); // s1
  if(v)
    show1("s1");
  W(p_i__ab1, 23, adr >> 1);
  wp(); // s2
  if(v)
    show1("s2");
  W(p_i__as1, 1, 0u);
  W(p_i__rw1, 1, 0u);
  wn(); // s3
  if(v)
    show1("s3");
  W(p_i__db1, 16, val);
  wp(); // s4
  if(v)
    show1("s4");
  W(p_i__uds1, 1, uds);
  W(p_i__lds1, 1, lds);
  while(R(p_o__dtack1)) {
    wn();
    if(v)
      show1();
    wp();
    if(v)
      show1();
  }
  wn(); // s5
  if(v)
    show1("s5");
  wp(); // s6
  if(v)
    show1("s6");
  wn(); // s7
  if(v)
    show1("s7");
  W(p_i__as1, 1, 1u);
  W(p_i__uds1, 1, 1u);
  W(p_i__lds1, 1, 1u);

  if(v)
    printf("Write cycle done\n");
}

u16 m68000_1_r(std::function<void ()> wp, std::function<void ()> wn, u32 adr, u8 uds, u8 lds, bool v = false)
{
  if(v)
    printf("Read cycle started %06x %d%d\n", adr, uds, lds);
  wp(); // s0
  if(v)
    show1("s0");
  W(p_i__rw1, 1, 1u);
  wn(); // s1
  if(v)
    show1("s1");
  W(p_i__ab1, 23, adr >> 1);
  wp(); // s2
  if(v)
    show1("s2");
  W(p_i__as1, 1, 0u);
  W(p_i__uds1, 1, uds);
  W(p_i__lds1, 1, lds);
  wn(); // s3
  if(v)
    show1("s3");
  wp(); // s4
  if(v)
    show1("s4");
  while(R(p_o__dtack1)) {
    wn();
    if(v)
      show1();
    wp();
    if(v)
      show1();
  }
  wn(); // s5
  if(v)
    show1("s5");
  wp(); // s6
  if(v)
    show1("s6");
  u16 val = R(p_o__db1);
  wn(); // s7
  if(v)
    show1("s7");
  W(p_i__as1, 1, 1u);
  W(p_i__uds1, 1, 1u);
  W(p_i__lds1, 1, 1u);

  if(v)
    printf("Read cycle done -> %04x\n", val);

  return val;
}


void m68000_2_w(std::function<void ()> wp, std::function<void ()> wn, u32 adr, u16 val, u8 uds, u8 lds, bool v = false)
{
  if(v)
    printf("Write cycle started %06x %04x %d%d\n", adr, val, uds, lds);
  wp(); // s0
  if(v)
    show2("s0");
  wn(); // s1
  if(v)
    show2("s1");
  W(p_i__ab2, 23, adr >> 1);
  wp(); // s2
  if(v)
    show2("s2");
  W(p_i__as2, 1, 0u);
  W(p_i__rw2, 1, 0u);
  wn(); // s3
  if(v)
    show2("s3");
  W(p_i__db2, 16, val);
  wp(); // s4
  if(v)
    show2("s4");
  W(p_i__uds2, 1, uds);
  W(p_i__lds2, 1, lds);
  while(R(p_o__dtack2)) {
    wn();
    if(v)
      show2();
    wp();
    if(v)
      show2();
  }
  wn(); // s5
  if(v)
    show2("s5");
  wp(); // s6
  if(v)
    show2("s6");
  wn(); // s7
  if(v)
    show2("s7");
  W(p_i__as2, 1, 1u);
  W(p_i__uds2, 1, 1u);
  W(p_i__lds2, 1, 1u);

  if(v)
    printf("Write cycle done\n");
}

u16 m68000_2_r(std::function<void ()> wp, std::function<void ()> wn, u32 adr, u8 uds, u8 lds, bool v = false)
{
  if(v)
    printf("Read cycle started %06x %d%d\n", adr, uds, lds);
  wp(); // s0
  if(v)
    show2("s0");
  W(p_i__rw2, 1, 1u);
  wn(); // s1
  if(v)
    show2("s1");
  W(p_i__ab2, 23, adr >> 1);
  wp(); // s2
  if(v)
    show2("s2");
  W(p_i__as2, 1, 0u);
  W(p_i__uds2, 1, uds);
  W(p_i__lds2, 1, lds);
  wn(); // s3
  if(v)
    show2("s3");
  wp(); // s4
  if(v)
    show2("s4");
  while(R(p_o__dtack2)) {
    wn();
    if(v)
      show2();
    wp();
    if(v)
      show2();
  }
  wn(); // s5
  if(v)
    show2("s5");
  wp(); // s6
  if(v)
    show2("s6");
  u16 val = R(p_o__db2);
  wn(); // s7
  if(v)
    show2("s7");
  W(p_i__as2, 1, 1u);
  W(p_i__uds2, 1, 1u);
  W(p_i__lds2, 1, 1u);

  if(v)
    printf("Read cycle done -> %04x\n", val);

  return val;
}

void run_design()
{
  W(p_i__uds1, 1, 1u);
  W(p_i__lds1, 1, 1u);
  W(p_i__as1,  1, 1u);
  W(p_i__ab1, 23, 0u);
  W(p_i__db1, 16, 0u);
  W(p_i__rw1,  1, 1u);
  W(p_i__uds2, 1, 1u);
  W(p_i__lds2, 1, 1u);
  W(p_i__as2,  1, 1u);
  W(p_i__ab2, 23, 0u);
  W(p_i__db2, 16, 0u);
  W(p_i__rw2,  1, 1u);

  reset();
  do
    wait_p6m();
  while(!(R(p_o__nvbk) & R(p_o__nhbk)));

  for(int i=0; i<100; i++)
    tick();

  for(const auto &e : rwrites)
    m68000_1_w(wait_n12m, wait_p12m, e.adr, e.data, e.uds, e.lds, false);

  for(u32 i=0; i<0x800; i++)
    m68000_1_w(wait_n12m, wait_p12m, 0x210000 + 2*i, roz_1_ram[2*i] << 8, 1, 0, false);

  for(u32 i=0; i<0x800; i++)
    m68000_1_w(wait_n12m, wait_p12m, 0x218000 + 2*i, roz_2_ram[2*i] << 8, 1, 0, false);

  
  int prev = 0x1010;

  for(;;) {
    wait_p6m();
    int next =
      (R(p_o__nvsy) << 12) |
      (R(p_o__nvbk) << 8) |
      (R(p_o__nhsy) << 4) |
      R(p_o__nhbk);

    if(next != prev) {
      if((prev & 0x100) && !(next & 0x100))
	break;
      prev = next;
    }

  }

  if(0)
    rozshow(263, 0);

  for(int x = 263; x >= 0; x--) {
    for(int y = 0; y != 384; y++) {

      u32 v = R(p_o__c0);
      u16 c = palette[v];

      u8 r = c & 31;
      u8 g = (c >> 5) & 31;
      u8 b = (c >> 10) & 31;

      //      r = inv<5>(r);
      //      g = inv<5>(g);

      unsigned int bcol = 0;
      bcol |= (r << 19) | ((r & 0x1c) << 14);
      bcol |= (g << 11) | ((g & 0x1c) <<  6);
      bcol |= (b <<  3) | ((b & 0x1c) >>  2);

      if(0) {
	if(v == 0x12)
	  bcol = 0xff0000;
	else if(v == 0x42)
	  bcol = 0x00ff00;
	else if(v == 0x40)
	  bcol = 0x0000ff;
	else if(v == 0x10)
	  bcol = 0x00ffff;
	else
	  bcol = 0xffffff;
      }

      if(0) {
	if(!R(p_o__nvbk))
	  bcol |= 0x00ffff;
	if(!R(p_o__nhbk))
	  bcol |= 0xff0000;
      }

      auto p1 = image + y*SY + x*SX + (264+1)*SX;

      unsigned int ccol = (p1[0] << 16) | (p1[1] << 8) | p1[2];

      auto p = image + y*SY + x*SX;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = bcol >> 16; p[4] = bcol >> 8; p[5] = bcol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;
      p += SY1;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = ccol >> 16; p[4] = ccol >> 8; p[5] = ccol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;
      p += SY1;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = bcol >> 16; p[4] = bcol >> 8; p[5] = bcol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;

#if 0
      do {
	tick();
	rozshow(x, y);
      } while(!R(p_o__p6m));
#else
      wait_p6m();
      if(0)
	rozshow(x, y);
#endif
    }
  }
}

char *selname;
int selid;

void run_trace()
{
  char tname[256];
  sprintf(tname, "captures/odn_%s.bin", selname);
  u64 *trace = (u64 *)file_load(tname);
  int pos = 0;

  for(int id=0; id != selid; id++) {
    pos++;
    while(!(trace[pos-1] & 0x0008000000000000) || (trace[pos] & 0x0008000000000000))
      pos++;
  }

  pos -= 384*16;

  for(int x = 263; x >= 0; x--) {
    for(int y = 0; y != 384; y++) {
      u64 v1 = trace[pos++];
      int v = ((v1 >> 56) & 0xff) | ((v1 >> 40) & 0x0700);
      u16 c = palette[v];
      u8 r = c & 31;
      u8 g = (c >> 5) & 31;
      u8 b = (c >> 10) & 31;

      unsigned int bcol = 0;
      bcol |= (r << 19) | ((r & 0x1c) << 14);
      bcol |= (g << 11) | ((g & 0x1c) <<  6);
      bcol |= (b <<  3) | ((b & 0x1c) >>  2);

      unsigned int ccol = bcol;
      if(!(v1 & 0x0008000000000000))
	ccol |= 0x00ffff;
      if(!(v1 & 0x0010000000000000))
	ccol |= 0xff0000;

      if(1)
      switch(v >> 8) {
      case 0: case 1: bcol = 0x0000ff; break; // obj
      case 2: case 3: bcol = 0x00ff00; break; // lvc1
      case 4: case 5: bcol = 0xff0000; break; // lvc2
	//      case 6:         bcol = 0xffff00; break; // roz1
	//      case 7:         bcol = 0xff00ff; break; // roz2
      }

      auto p = image + y*SY + x*SX + (264 + 1)*SX;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = bcol >> 16; p[4] = bcol >> 8; p[5] = bcol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;
      p += SY1;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = ccol >> 16; p[4] = ccol >> 8; p[5] = ccol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;
      p += SY1;
      p[0] = bcol >> 16; p[1] = bcol >> 8; p[2] = bcol;
      p[3] = bcol >> 16; p[4] = bcol >> 8; p[5] = bcol;
      p[6] = bcol >> 16; p[7] = bcol >> 8; p[8] = bcol;
    }
  }
}


int main(int argc, char **argv)
{
  if(argc != 3) {
    fprintf(stderr, "Usage:\n%s <scene> <id>\n", argv[0]);
    exit(1);
  }

  selname = argv[1];
  selid = strtol(argv[2], nullptr, 10);

  memset(image, 0, sizeof(image));

  for(int y=0; y<384; y++) {
    auto p = image + SY*y + 264*SX + 3;
    for(int yy=0; yy<3; yy++) {
      memset(p, 0xff, 3);
      p += SY1;
    }
  }

  char path[4096];
  sprintf(path, "captures/%s_%d_pal.bin", selname, selid);
  palette = static_cast<u16 *>(file_load(path));
  for(int i=0; i != 2048; i++)
    palette[i] = (palette[i] << 8) | (palette[i] >> 8);

  sprintf(path, "captures/%s_%d_roz_1.bin", selname, selid);
  roz_1_ram = static_cast<u8 *>(file_load(path));

  sprintf(path, "captures/%s_%d_roz_2.bin", selname, selid);
  roz_2_ram = static_cast<u8 *>(file_load(path));

  sprintf(path, "captures/%s_%d_lvc.bin", selname, selid);
  lvc_ram = static_cast<u8 *>(file_load(path));

  char line[4096];

  sprintf(path, "captures/%s_%d_regs.txt", selname, selid);
  FILE *rfd = fopen(path, "r");
  while(fgets(line, sizeof(line), rfd)) {
    //      for(int i=0; line[i]; i++)
    //	  printf("%03d: %02x %c\n", i, line[i], line[i]);
    assert(line[1] == ' ');
    assert(line[8] == ' ');
    line[8] = 0;
    line[13] = 0;
    u8 id = line[0] == 'b';
    u32 adr = strtol(line+2, nullptr, 16);
    u16 v1 = strtol(line+9, nullptr, 16);
    u8 v2 = strtol(line+11, nullptr, 16);
    if(line[9] == '.')
      rwrites.emplace_back(rwrite{ adr, v2, 0, 1, id });
    else if(line[11] == '.')
      rwrites.emplace_back(rwrite{ adr, u16(v1 << 8), 1, 0, id });
    else
      rwrites.emplace_back(rwrite{ adr, v1, 1, 1, id });
  }
  fclose(rfd);


  run_trace();
  run_design();

  char pngname[256];
  sprintf(pngname, "%s_%d.png", selname, selid);

  png_write(pngname, image, (264*2+1)*3, 384*3);

  return 0;
}
