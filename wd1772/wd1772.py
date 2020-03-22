from nmigen import *

class Firmware(Elaboratable):
    def __init__(self):
        self.i_clka0  = Signal()
        self.i_clka1  = Signal()
        self.i_romadr = Signal(8)
        self.o_romout = Signal(19)
        self.mem      = Memory(width=19, depth=256, init=[
            0x54800, 0x24290, 0x28fe0, 0x00058, 0x00098, 0x04198, 0x0c9d0, 0x4c9d0,
            0x3c200, 0x24202, 0x30e58, 0x58270, 0x3c200, 0x18400, 0x10232, 0x24204,
            0x00758, 0x50374, 0x00758, 0x50374, 0x78600, 0x305d8, 0x30e00, 0x00a30,
            0x28336, 0x00ab0, 0x303b7, 0x0038b, 0x24310, 0x243f8, 0x7ffff, 0x7ffff,
            0x24390, 0x24260, 0x28230, 0x2c358, 0x54890, 0x48332, 0x088b0, 0x2c9a0,
            0x2c920, 0x402b6, 0x589b0, 0x48600, 0x701b8, 0x00379, 0x7cc00, 0x40138,
            0x48349, 0x60db0, 0x50948, 0x40038, 0x24ce8, 0x34d40, 0x481b8, 0x48820,
            0x48349, 0x6c2a2, 0x00ab0, 0x00b88, 0x1834c, 0x00000, 0x7ffff, 0x7ffff,
            0x40600, 0x30400, 0x40728, 0x30400, 0x282f5, 0x083f1, 0x40600, 0x30400,
            0x68331, 0x20370, 0x14204, 0x502b6, 0x48349, 0x00000, 0x48600, 0x60160,
            0x30e00, 0x00b48, 0x68600, 0x50400, 0x00ba9, 0x18600, 0x50400, 0x00b49,
            0x00000, 0x00000, 0x10600, 0x30400, 0x083f1, 0x30600, 0x30400, 0x0c201,
            0x40140, 0x40000, 0x40000, 0x40000, 0x582cc, 0x58400, 0x74d40, 0x5b440,
            0x20348, 0x47000, 0x47140, 0x7334b, 0x7ffff, 0x7ffff, 0x7ffff, 0x7ffff,
            0x02000, 0x22ce8, 0x5a468, 0x20348, 0x023af, 0x2234f, 0x5a400, 0x22d48,
            0x12600, 0x524e8, 0x20250, 0x4034a, 0x7ffff, 0x7ffff, 0x7ffff, 0x7ffff,
            0x0aba9, 0x1a410, 0x48b49, 0x42600, 0x525c8, 0x42b48, 0x42410, 0x42b48,
            0x42428, 0x42b48, 0x02a18, 0x12a34, 0x7ad30, 0x42168, 0x0a34f, 0x0a1b8,
            0x32b4c, 0x70600, 0x58b4a, 0x52410, 0x52d48, 0x0a1b8, 0x02a20, 0x42400,
            0x0a160, 0x7aa34, 0x02a20, 0x7ab4c, 0x00000, 0x00000, 0x00000, 0x46400,
            0x42400, 0x42400, 0x02a50, 0x00000, 0x40460, 0x20230, 0x202b5, 0x40540,
            0x40b4c, 0x00000, 0x00000, 0x00000, 0x00000, 0x50400, 0x582cc, 0x08bab,
            0x68600, 0x20e00, 0x50400, 0x6d600, 0x550e0, 0x01000, 0x05000, 0x01078,
            0x05000, 0x05000, 0x05000, 0x05000, 0x51b86, 0x19b4b, 0x7ffff, 0x7ffff,
            0x42400, 0x52bad, 0x42400, 0x52410, 0x42b48, 0x525c8, 0x42b48, 0x62b4d,
            0x1a428, 0x0034a, 0x02a18, 0x12a34, 0x7ad30, 0x42168, 0x0a34f, 0x0a1b8,
            0x32b4c, 0x70600, 0x58b4a, 0x52410, 0x42b48, 0x52428, 0x02b48, 0x4aa1d,
            0x02b48, 0x6aa1d, 0x1ad48, 0x1ac90, 0x12e00, 0x02150, 0x424e8, 0x3a700,
            0x524e8, 0x02b83, 0x42000, 0x42000, 0x20250, 0x00460, 0x403b2, 0x38349,
            0x40000, 0x55600, 0x550e0, 0x01078, 0x11e00, 0x11e00, 0x11e00, 0x11e00,
            0x65bf7, 0x3d600, 0x55dc0, 0x39600, 0x51dc0, 0x03150, 0x03100, 0x53540,
            0x73b87, 0x43000, 0x47000, 0x47000, 0x41000, 0x50b4b, 0x7ffff, 0x7ffff
            ])

    def elaborate(self, platform):
        m = Module()
        m.submodules.rdport = rdport = self.mem.read_port()
        with m.If(self.i_clka0):
            m.d.sync += rdport.addr.eq(self.i_romadr)
        with m.If(self.i_clka1):
            m.d.sync += self.o_romout.eq(rdport.data)
        return m

class PC(Elaboratable):
    def __init__(self):
        self.o_pc = Signal(8)
        self.i_rom = Signal(19)
        self.i_pch_set_rom = Signal()
        self.i_pch_set_next = Signal()
        self.i_pcl_set_rom = Signal()
        self.i_pcl_set_next = Signal()

    def elaborate(self, platform):
        m = Module()

        return m

class PLL(Elaboratable):
    def __init__(self):
        self.i_clks0   = Signal()
        self.i_clks1   = Signal()

        self.i_rd      = Signal()
        self.i_mr      = Signal()
        self.i_pll_on  = Signal()

        self.o_rdstate = Signal()
        self.o_clka0   = Signal()
        self.o_clka1   = Signal()
        self.o_clkb0   = Signal()
        self.o_clkb1   = Signal()
        self.o_n252    = Signal()
        self.o_n1416   = Signal()
        self.o_wd      = Signal()
        
        self.pll_on_d  = Signal()
        self.pll_on_d2 = Signal()
        self.clka      = Signal()
        self.clkb      = Signal()

        self.n853      = Signal()
        self.n1027     = Signal()
        self.n1050     = Signal()
        self.n1079     = Signal()
        self.n1105     = Signal()
        self.n1130     = Signal()
        self.n1162     = Signal()
        self.n1192     = Signal()
        self.n1227     = Signal()
        self.n1266     = Signal()
        self.n1292     = Signal()
        self.rdp       = Signal()
        self.n1246     = Signal()
        self.n1238     = Signal()
        self.n1268     = Signal()
        self.n1282     = Signal()
        self.n1298     = Signal()
        self.n1312     = Signal()
        self. n283     = Signal()
        self. n257     = Signal()
        self. n259     = Signal()
        self. n253     = Signal()
        self.n1045     = Signal()
        self.n1047     = Signal()
        self.  n35     = Signal()
        self.n1119     = Signal()
        self.n1122     = Signal()
        self.n1031     = Signal()
        self.n1206     = Signal()
        self.n1208     = Signal()
        self.n1114     = Signal()
        self.n1284     = Signal()
        self.n1195     = Signal()
        self.n1341     = Signal()
        self.n1240     = Signal()
        self.n1438     = Signal()
        self.n1155     = Signal()
        self.n1297     = Signal()
        self.n1073     = Signal()
        self.n1220     = Signal()
        self.n1221     = Signal()
        self. n910     = Signal()
        self.n1135     = Signal()
        self.n1136     = Signal()
        self. n850     = Signal()
        self.n1059     = Signal()
        self.n1060     = Signal()
        self. n289     = Signal()
        self. n732     = Signal()
        self. n731     = Signal()
        self. n227     = Signal()
        self. n265     = Signal()
        self. n266     = Signal()
        self.  n36     = Signal()
        self.n1384     = Signal()
        self.n1415     = Signal()
        self.n1439     = Signal()
        self.n1465     = Signal()
        self.n1388     = Signal()
        self.n1422     = Signal()
        self.n1447     = Signal()
        self.n1463     = Signal()
        self. n232     = Signal()
        self.  n55     = Signal()
        self. n545     = Signal()
        self. n661     = Signal()
        self. n663     = Signal()
        self.  n62     = Signal()
        self. n229     = Signal()
        self. n220     = Signal()
        self. n193     = Signal()
        self.  n56     = Signal()
        self. n122     = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.o_clka0):
            m.d.sync += self.o_clka0.eq(0)
        with m.If(self.o_clka1):
            m.d.sync += self.o_clka1.eq(0)
        with m.If(self.o_clkb0):
            m.d.sync += self.o_clkb0.eq(0)
        with m.If(self.o_clkb1):
            m.d.sync += self.o_clkb1.eq(0)

        with m.If(self.o_clka1):
            m.d.sync += self.pll_on_d.eq(~self.i_pll_on)

        with m.If(self.o_clka0):
            m.d.sync += self.pll_on_d2.eq(~self.pll_on_d)

        n733 = Signal()
        m.d.comb += n733.eq(self.i_mr & ~self.pll_on_d2)

        with m.If(self.i_clks1):
            m.d.sync += self.n853.eq(n733 & ~self.i_rd)
            m.d.sync += self.n1050.eq(self.n1027)
            m.d.sync += self.n1105.eq(self.n1079)
            m.d.sync += self.n1162.eq(self.n1130)
            m.d.sync += self.n1227.eq(self.n1192)
            m.d.sync += self.n1292.eq(self.n1266)
            m.d.sync += self.n1238.eq(self.rdp)
            m.d.sync += self.n1268.eq(~self.n1246)
            m.d.sync += self.n1298.eq(~self.n1282)

        with m.If(self.i_clks0):
            m.d.sync += self.n1027.eq(self.n853)
            m.d.sync += self.n1079.eq(self.n1050)
            m.d.sync += self.n1130.eq(self.n1105)
            m.d.sync += self.n1192.eq(self.n1162)
            m.d.sync += self.n1266.eq(self.n1227)
            m.d.sync += self.rdp.eq(self.n1292 & self.n1227)
            m.d.sync += self.n1246.eq(~self.n1238)
            m.d.sync += self.n1282.eq(~self.n1268)
            m.d.sync += self.n1312.eq(~self.n1298)
            with m.If(self.n1238):
                m.d.sync += self.o_rdstate.eq(1)
            with m.Elif(self.n1298):
                m.d.sync += self.o_rdstate.eq(0)

        with m.If(self.i_clks1):
            m.d.sync += self. n257.eq(~(self.rdp  | self.n232))
            m.d.sync += self. n259.eq(~(self.n253 | self.n232))
        with m.If(self.i_clks0):
            m.d.sync += self. n253.eq(~(self.n55  | self.n257  | self.n259))

        with m.If(self.i_clks1):
            m.d.sync += self. n661.eq(~(self.rdp  | self.n253))
            m.d.sync += self. n663.eq(~(~self.rdp | self.n545))
        with m.If(self.i_clks0):
            m.d.sync += self. n545.eq(~(self.n55  | self.n661  | self.n663))

        with m.If(self.i_clks1):
            m.d.sync += self.n1045.eq(~(self.rdp  | self.n545 ))
            m.d.sync += self.n1047.eq(~(~self.rdp | self.n35   | self.n1031))
        with m.If(self.i_clks0):
            m.d.sync += self.  n35.eq(~(self.n55  | self.n1045 | self.n1047))
            with m.If((~self.clka) & ~(self.n55  | self.n1045 | self.n1047)):
                m.d.sync += self.o_n252.eq(0)
                m.d.sync += self.clka.eq(1)
                m.d.sync += self.o_clka1.eq(1)

        with m.If(self.i_clks1):
            m.d.sync += self.n1119.eq(~(self.rdp  | self.n35  ))
            m.d.sync += self.n1122.eq(~(~self.rdp | self.n1114))
        with m.If(self.i_clks0):
            m.d.sync += self.n1031.eq(~(self.n55  | self.n1119 | self.n1122))

        with m.If(self.i_clks1):
            m.d.sync += self.n1206.eq(~(self.rdp  | self.n1031))
            m.d.sync += self.n1208.eq(~(~self.rdp | self.n1195))
        with m.If(self.i_clks0):
            m.d.sync += self.n1114.eq(~(self.n55  | self.n1206 | self.n1208))

        with m.If(self.i_clks1):
            m.d.sync += self.n1284.eq(~(~self.rdp & self.n1114))
        with m.If(self.i_clks0):
            m.d.sync += self.n1195.eq(~(self.n55  | self.n1284))

        with m.If(self.i_clks1):
            m.d.sync += self.n1341.eq(~(~self.rdp & self.n1195))
        with m.If(self.i_clks0):
            m.d.sync += self.n1240.eq(~(self.n55  | self.n1341))
            with m.If(~(self.n55  | self.n1341)):
                m.d.sync += self.o_n1416.eq(self.n283)
            with m.If((~self.clkb) & ~(self.n55  | self.n1341)):
                m.d.sync += self.clkb.eq(1)
                m.d.sync += self.o_clkb1.eq(1)

        with m.If(self.i_clks1):
            m.d.sync += self.n1438.eq(~(~self.rdp & self.n1240))
        with m.If(self.i_clks0):
            m.d.sync += self.n1155.eq(~(self.n55  | self.n1438))

        with m.If(self.i_clks1):
            m.d.sync += self.n1297.eq(~(~self.rdp & self.n1155))
        with m.If(self.i_clks0):
            m.d.sync += self.n1073.eq(~(self.n55  | self.n1297))

        with m.If(self.i_clks1):
            m.d.sync += self.n1220.eq(~(self.rdp  | self.n1073))
            m.d.sync += self.n1221.eq(~(~self.rdp | self.n1240))
        with m.If(self.i_clks0):
            m.d.sync += self. n910.eq(~(self.n55  | self.n1220 | self.n1221))

        with m.If(self.i_clks1):
            m.d.sync += self.n1135.eq(~(self.rdp  | self.n910  | self.n850 ))
            m.d.sync += self.n1136.eq(~(~self.rdp | self.n1155))
        with m.If(self.i_clks0):
            m.d.sync += self. n850.eq(~(self.n55  | self.n1135 | self.n1136))

        with m.If(self.i_clks1):
            m.d.sync += self.n1059.eq(~(self.rdp  | self.n850 ))
            m.d.sync += self.n1060.eq(~(~self.rdp | self.n1073))
        with m.If(self.i_clks0):
            m.d.sync += self. n289.eq(~(self.n55  | self.n1059 | self.n1060))

        with m.If(self.i_clks1):
            m.d.sync += self. n732.eq(~(self.rdp  | self.n289 ))
            m.d.sync += self. n731.eq(~(~self.rdp | self.n850 ))
        with m.If(self.i_clks0):
            m.d.sync += self. n227.eq(~(self.n55  | self.n732  | self.n731))

        with m.If(self.i_clks1):
            m.d.sync += self. n265.eq(~(self.rdp  | self.n227 ))
            m.d.sync += self. n266.eq(~(~self.rdp | self.n289 ))
        with m.If(self.i_clks0):
            m.d.sync += self.  n36.eq(~(self.n55  | self.n265  | self.n266))

        with m.If(self.i_clks1):
            m.d.sync += self.n1384.eq(~self.n1240)
            m.d.sync += self.n1415.eq(~self.n1388)
            m.d.sync += self.n1439.eq(~self.n1422)
            m.d.sync += self.n1465.eq(~self.n1447)

        with m.If(self.i_clks0):
            m.d.sync += self.n1388.eq(~self.n1384)
            m.d.sync += self.n1422.eq(~self.n1415)
            m.d.sync += self.n1447.eq(~self.n1439)
            m.d.sync += self.n1463.eq(~self.n1465)
            with m.If(~self.n1465):
                with m.If(self.clka):
                    m.d.sync += self.clka.eq(0)
                    m.d.sync += self.o_clka0.eq(1)
                with m.If(self.clkb):
                    m.d.sync += self.clkb.eq(0)
                    m.d.sync += self.o_clkb0.eq(1)

        m.d.comb += self.n62.eq(~(self.n232 | self.n253 | self.n545 | self.n35 | self.n1031 | self.n1114 | self.n1195 | self.n1240 | self.n1155 | self.n1073 | self.n910 | self.n850 | self.n289 | self.n227 | self.n36))

        with m.If(self.i_clks1):
            m.d.sync += self.n229.eq(self.n36)
            m.d.sync += self.n220.eq(self.n227 & self.rdp)
            m.d.sync += self.n193.eq(~self.n56 ^ self.n62)
            m.d.sync += self.n122.eq(~self.n56)

        m.d.comb += self.n55.eq(~self.n193)

        with m.If(self.i_clks0):
            m.d.sync += self.n56.eq(self.n229 | self.n220 | ~self.n193)
            m.d.sync += self.n232.eq(~(self.n55 | self.n122))
            with m.If(self.n229 | self.n220 | ~self.n193):
                m.d.sync += self.o_n252.eq(1)
                m.d.sync += self.o_wd.eq(0)
                m.d.sync += self.n283.eq(~self.o_n1416)

        return m

            

class wd1772(Elaboratable):
    def __init__(self):
        self.i_clkp    = Signal()
        self.i_clkn    = Signal()

        self.i_mr      = Signal()
        self.i_rd      = Signal()

        self.o_wd      = Signal()

        self.clks0     = Signal()
        self.clks1     = Signal()

        self.fm_enable = Signal()
        self.fm_tick   = Signal()
        self.pll_on    = Signal()

    def elaborate(self, platform):
        m = Module()
#        m.submodules.firmware = firmware = Firmware()
        m.submodules.pll      = pll      = PLL()

        m.d.comb += pll.i_clks0.eq(self.clks0)
        m.d.comb += pll.i_clks1.eq(self.clks1)
        m.d.comb += pll.i_mr.eq(self.i_mr)
        m.d.comb += pll.i_rd.eq(self.i_rd)
        m.d.comb += pll.i_pll_on.eq(0)
        m.d.comb += self.o_wd.eq(pll.o_wd)

        with m.If(self.i_clkp):
            m.d.sync += self.fm_tick.eq(~self.fm_tick)

        with m.If(self.fm_enable):
            m.d.comb += self.clks1.eq(self.i_clkp &  self.fm_tick)
            m.d.comb += self.clks0.eq(self.i_clkp & ~self.fm_tick)
        with m.Else():
            m.d.comb += self.clks1.eq(self.i_clkp)
            m.d.comb += self.clks0.eq(self.i_clkn)
        
        return m
