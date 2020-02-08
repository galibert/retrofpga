#include <stdio.h>
#include "overdrive.cc"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <zlib.h>

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

u16 *palette;

u16 vram[0x20*0x20];

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

void run_design()
{
  cxxrtl_design::p_overdrive overdrive;

  //  overdrive.p_i__ccs.next = value<1>{1u};
  //  overdrive.step();

  int prev = 0x1010;

  for(;;) {
    int next =
      (overdrive.p_o__nvsy.curr.data[0] << 12) |
      (overdrive.p_o__nvbk.curr.data[0] << 8) |
      (overdrive.p_o__nhsy.curr.data[0] << 4) |
      overdrive.p_o__nhbk.curr.data[0];

    if(next != prev) {
      if((prev & 0x100) && !(next & 0x100))
	break;
      prev = next;
    }

    // more compatible but slightly slower code: explicitly drive a clock signal
    //    overdrive.p_clk.next = value<1>{1u};
    //    overdrive.step();
    //    overdrive.p_clk.next = value<1>{0u};
    //    overdrive.step();
    // less compatible but slightly faster code: trigger events directly
    // overdrive.posedge_p_clk = true;
    // overdrive.step();
    // even less compatible but even faster code: omit delta cycles

    overdrive.posedge_p_clk = true;
    overdrive.eval();
    overdrive.commit();
  }

  for(int x = 263; x >= 0; x--) {
    for(int y = 0; y != 384; y++) {
      u32 v = overdrive.p_o__ci4.curr.data[0];
      u16 c = palette[v | 0x600];
      printf("%03d.%03d.a: ca=%06x xcp=%06x ycp=%06x vramadr=%03x\n", x, y, overdrive.p_o__ca.curr.data[0], overdrive.p_o__xcp.curr.data[0], overdrive.p_o__ycp.curr.data[0], overdrive.p_o__vramadr.curr.data[0]);
      //      c = overdrive.p_o__vramadr.curr.data[0];

      u8 r = c & 31;
      u8 g = (c >> 5) & 31;
      u8 b = (c >> 10) & 31;

      //      r = inv<5>(r);
      //      g = inv<5>(g);

      unsigned int bcol = 0;
      bcol |= (r << 19) | ((r & 0x1c) << 14);
      bcol |= (g << 11) | ((g & 0x1c) <<  6);
      bcol |= (b <<  3) | ((b & 0x1c) >>  2);

      //      bcol = 0;
      //      u16 vr = vram[c];
      //      printf("%03x\n", c);
      //      bcol = (inv<8>(vr >> 8) << 16) | (inv<8>(vr) << 8);


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
	if(!overdrive.p_o__nvbk.curr.data[0])
	  bcol |= 0x00ffff;
	if(!overdrive.p_o__nhbk.curr.data[0])
	  bcol |= 0xff0000;
      }

      unsigned int ccol = 0;
      if(!overdrive.p_o__nvsy.curr.data[0])
	ccol |= 0x00ffff;
      if(!overdrive.p_o__nhsy.curr.data[0])
	ccol |= 0xff0000;

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
      
      overdrive.posedge_p_clk = true;
      overdrive.eval();
      overdrive.commit();

      printf("%03d.%03d.b: ca=%06x xcp=%06x ycp=%06x vramadr=%03x\n", x, y, overdrive.p_o__ca.curr.data[0], overdrive.p_o__xcp.curr.data[0], overdrive.p_o__ycp.curr.data[0], overdrive.p_o__vramadr.curr.data[0]);

      overdrive.posedge_p_clk = true;
      overdrive.eval();
      overdrive.commit();
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
      case 6:         bcol = 0xffff00; break; // roz1
      case 7:         bcol = 0xff00ff; break; // roz2
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

  u8 *vr = static_cast<u8 *>(file_load("captures/first_1_roz_1.bin"));
  for(int i=0; i<0x20*0x20; i++)
    vram[i] = vr[2*i] | (vr[2*i+0x800] << 8);

  run_design();
  run_trace();

  char pngname[256];
  sprintf(pngname, "%s_%d.png", selname, selid);

  png_write(pngname, image, (264*2+1)*3, 384*3);

  return 0;
}
