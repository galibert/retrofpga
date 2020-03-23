from nmigen import *

class Firmware(Elaboratable):
    def __init__(self):
        self.i_clka0   = Signal()
        self.i_clka1   = Signal()
        self.i_rom_adr = Signal(8)
        self.o_rom_out = Signal(19)
        self.mem       = Memory(width=19, depth=256, init=[
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
        m.d.comb += rdport.addr.eq(self.i_rom_adr)
        with m.If(self.i_clka0):
            m.d.sync += self.o_rom_out.eq(~rdport.data)
        return m

class PC(Elaboratable):
    def __init__(self):
        self.i_clka0       = Signal()
        self.i_clka1       = Signal()
        self.i_rom_out     = Signal(19)
        self.i_global_test = Signal()
        self.i_n1454       = Signal()
        self.i_cmd_restore = Signal()
        self.i_reset       = Signal()

        self.o_rom_adr     = Signal(8)

        self.pc_hold       = Signal(8)
        self.pc_rom        = Signal(8)
        self.pc_next       = Signal(8)

        self.pch_set       = Signal(2)
        self.pcl_set       = Signal(2)
        self.jump          = Signal(4)

        self.cmd_restore_h = Signal()
        self.global_test_h = Signal()
        self.sel_h         = Signal()
        self.n1454_h       = Signal()
        self.r9_h          = Signal()
        self.r10_h         = Signal()
        self.pc_reset      = Signal()

    def elaborate(self, platform):
        m = Module()

        pjump = Signal()
        
        with m.If(self.i_clka0):
            m.d.sync += self.cmd_restore_h.eq(self.i_cmd_restore)
        m.d.comb += pjump.eq(self.cmd_restore_h & self.i_rom_out[9] & (self.i_rom_out[10] ^ self.i_rom_out[11]))

        with m.If(self.i_clka1):
            m.d.sync += self.jump[1].eq(pjump)

        with m.Switch(self.pcl_set):
            with m.Case(0):
                m.d.comb += self.o_rom_adr[:4].eq(self.pc_rom[:4] | self.pc_next[:4] | self.jump)
            with m.Case(1):
                m.d.comb += self.o_rom_adr[:4].eq(self.pc_next[:4] | self.jump)
            with m.Case(2):
                m.d.comb += self.o_rom_adr[:4].eq(self.pc_rom[:4] | self.jump)
            with m.Case(3):
                m.d.comb += self.o_rom_adr[:4].eq(self.jump)

        with m.Switch(self.pch_set):
            with m.Case(0):
                m.d.comb += self.o_rom_adr[4:].eq(self.pc_rom[4:] | self.pc_next[4:])
            with m.Case(1):
                m.d.comb += self.o_rom_adr[4:].eq(self.pc_next[4:])
            with m.Case(2):
                m.d.comb += self.o_rom_adr[4:].eq(self.pc_rom[4:])
            with m.Case(3):
                m.d.comb += self.o_rom_adr[4:].eq(0)
        
        with m.If(self.i_clka0):
            m.d.sync += self.pc_hold.eq(self.o_rom_adr)

        with m.If(self.i_clka1):
            m.d.sync += self.pc_rom[0].eq(~self.i_rom_out[18])
            m.d.sync += self.pc_rom[1].eq(~self.i_rom_out[17])
            m.d.sync += self.pc_rom[2].eq(~self.i_rom_out[16])
            m.d.sync += self.pc_rom[3].eq(~self.i_rom_out[15])
            m.d.sync += self.pc_rom[4].eq(~self.i_rom_out[ 2])
            m.d.sync += self.pc_rom[5].eq(~self.i_rom_out[ 1])
            m.d.sync += self.pc_rom[6].eq(~self.i_rom_out[ 0])
            m.d.sync += self.pc_rom[7].eq(~self.i_rom_out[11])

            m.d.sync += self.pc_next.eq(self.pc_hold + (self.i_global_test & self.i_n1454))

            m.d.sync += self.global_test_h.eq(self.i_global_test)
            m.d.sync += self.sel_h.eq((self.i_rom_out[9] & ~self.i_rom_out[11]) | (~self.i_rom_out[9] & self.i_rom_out[10]))
            m.d.sync += self.n1454_h.eq(self.i_n1454)
            m.d.sync += self.r9_h.eq(self.i_rom_out[9])
            m.d.sync += self.r10_h.eq(self.i_rom_out[9])
            m.d.sync += self.pc_reset.eq(self.i_reset | pjump)

        pcl_next = Signal()
        m.d.comb += pcl_next.eq(self.sel_h & self.n1454_h & ~self.global_test_h)
        m.d.comb += self.pcl_set[0].eq(self.pc_reset | ~pcl_next)
        m.d.comb += self.pcl_set[1].eq(self.pc_reset | pcl_next)

        pch_next = Signal()
        m.d.comb += pch_next.eq(self.r10_h & ~self.r9_h & self.n1454_h & ~self.global_test_h)
        m.d.comb += self.pch_set[0].eq(self.pc_reset | ~pch_next)
        m.d.comb += self.pch_set[1].eq(self.pc_reset | pch_next)
        return m

class Stepping(Elaboratable):
    def __init__(self):
        self.i_clka0       = Signal()
        self.i_clka1       = Signal()
        self.i_rom_out     = Signal(19)
        self.i_tr00        = Signal()

        self.o_step        = Signal()
        self.o_dirc        = Signal()
        self.o_test        = Signal()

        self.step_h        = Signal()
        self.dirc_h        = Signal()
        self.tr00_h        = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.i_clka1):
            m.d.sync += self.step_h.eq(self.i_rom_out[3:9] == 0x1a)
            m.d.sync += self.dirc_h.eq((self.i_rom_out[3:8] == 0x1b))

        with m.If(self.i_clka0):
            m.d.sync += self.o_step.eq(self.step_h)
            m.d.sync += self.o_dirc.eq(self.dirc_h)
            m.d.sync += self.tr00_h.eq(self.i_tr00)

        m.d.comb += self.o_test.eq((self.i_rom_out[3:9] == 0x10) & (~self.tr00_h | self.o_dirc))

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

        self.i_cs      = Signal()
        self.i_rw      = Signal()
        self.i_a       = Signal(2)
        self.i_dal     = Signal(8)
        self.o_dal     = Signal(8)
        self.i_mr      = Signal()
        self.o_step    = Signal()
        self.o_dirc    = Signal()
        self.i_rd      = Signal()
        self.o_mo      = Signal()
        self.o_wg      = Signal()
        self.o_wd      = Signal()
        self.i_tr00    = Signal()
        self.i_ip      = Signal()
        self.i_wprt    = Signal()
        self.i_dden    = Signal()
        self.o_drq     = Signal()
        self.o_intrq   = Signal()


        self.clks0     = Signal()
        self.clks1     = Signal()

        self.fm_enable = Signal()
        self.fm_tick   = Signal()
        self.pll_on    = Signal()
        self.reset     = Signal()
        self.reset_h   = Signal()
        self.tr00      = Signal()
        self.tr00_h    = Signal()
        self.index     = Signal()
        self.index_h   = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.firmware = firmware = Firmware()
        m.submodules.pll      = pll      = PLL()
        m.submodules.pc       = pc       = PC()
        m.submodules.stepping = stepping = Stepping()

        test = Signal()
        wprt = Signal()
        m.d.comb += wprt.eq((firmware.o_rom_out[3:9] == 0x0e) & self.i_wprt)
        m.d.comb += test.eq((firmware.o_rom_out[12:15] != 3) & ~stepping.o_test & ~wprt)

        m.d.comb += pll.i_clks0.eq(self.clks0)
        m.d.comb += pll.i_clks1.eq(self.clks1)
        m.d.comb += pll.i_mr.eq(self.i_mr)
        m.d.comb += pll.i_rd.eq(self.i_rd)
        m.d.comb += self.o_wd.eq(pll.o_wd)

        m.d.comb += pc.i_clka0.eq(pll.o_clka0)
        m.d.comb += pc.i_clka1.eq(pll.o_clka1)
        m.d.comb += pc.i_rom_out.eq(firmware.o_rom_out)
        m.d.comb += pc.i_reset.eq(self.reset)
        m.d.comb += pc.i_global_test.eq(test)

        m.d.comb += pc.i_cmd_restore.eq(0)
        m.d.comb += pc.i_n1454.eq(1)

        m.d.comb += firmware.i_rom_adr.eq(pc.o_rom_adr)
        m.d.comb += firmware.i_clka0.eq(pll.o_clka0)
        m.d.comb += firmware.i_clka1.eq(pll.o_clka1)

        m.d.comb += stepping.i_clka0.eq(pll.o_clka0)
        m.d.comb += stepping.i_clka1.eq(pll.o_clka1)
        m.d.comb += stepping.i_rom_out.eq(firmware.o_rom_out)
        m.d.comb += stepping.i_tr00.eq(self.tr00)
        m.d.comb += self.o_step.eq(stepping.o_step)
        m.d.comb += self.o_dirc.eq(stepping.o_dirc)

        with m.If(self.fm_enable):
            m.d.comb += self.clks1.eq(self.i_clkp &  self.fm_tick)
            m.d.comb += self.clks0.eq(self.i_clkp & ~self.fm_tick)
        with m.Else():
            m.d.comb += self.clks1.eq(self.i_clkp)
            m.d.comb += self.clks0.eq(self.i_clkn)


        with m.If(pll.o_clka1):
            m.d.sync += self.reset_h.eq(self.i_mr)
            m.d.sync += self.tr00_h.eq(self.i_tr00)
            m.d.sync += self.index_h.eq(self.i_ip)
        with m.If(pll.o_clka0):
            m.d.sync += self.reset.eq(~self.reset_h)
            m.d.sync += self.tr00.eq(~self.tr00_h)
            m.d.sync += self.index.eq(~self.index_h)

        with m.If(self.i_clkp):
            m.d.sync += self.fm_tick.eq(~self.fm_tick)

        # n1214 = !pll_on
        m.d.comb += pll.i_pll_on.eq(firmware.o_rom_out[12:14] == 1)
        return m
