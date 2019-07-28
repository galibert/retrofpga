from nmigen import *

class firmware(Elaboratable):
    def __init__(self):
        self.i_adr = Signal(8)
        self.o_rom = Signal(19)
        self.mem = Memory(width=19, depth=256, init=[
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
        m.submodules.rdport = rdport = self.mem.read_port(domain="ck0n")
        m.d.ck0n += [ rdport.addr.eq(self.i_adr), self.o_rom.eq(rdport.data) ]
        return m

class wd1772(Elaboratable):
    def __init__(self):
        self.ck0p = ClockDomain()
        self.ck0n = ClockDomain()
        self.m_firmware = firmware()
        self.i_adr = Signal(8)
        self.o_rom = Signal(19)

    def elaborate(self, platform):
        m = Module()
        m.domains += self.ck0p, self.ck0n
        m.d.comb += [ self.m_firmware.i_adr.eq(self.i_adr), self.o_rom.eq(self.m_firmware.o_rom) ]
        return m
