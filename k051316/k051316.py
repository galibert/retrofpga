from nmigen import *

class k051316(Elaboratable):
    def __init__(self):
        self.i_p12m  = Signal()
        self.i_n12m  = Signal()
        self.i_p6m  = Signal()
        self.i_n6m  = Signal()

        self.i_ab = Signal(11)
        self.i_db = Signal(8)
        self.i_vrcs = Signal()
        self.i_iocs = Signal()
        self.i_rw = Signal()
        self.i_nhsy = Signal()
        self.i_nhbk = Signal()
        self.i_nvsy = Signal()
        self.i_nvbk = Signal()

        self.o_db = Signal(8, reset = 0xff)

        self.o_ca = Signal(24)
        self.o_oblk = Signal()

        self.o_vramadr = Signal(10)
        self.o_rdata = Signal(16)
        self.o_vramen = Signal()
        self.o_xcp = Signal(24)
        self.o_ycp = Signal(24)
        self.o_start_x = Signal(16)
        self.o_incxx = Signal(16)

        self.start_x = Signal(signed(16))
        self.incxx   = Signal(signed(16))
        self.incyx   = Signal(signed(16))
        self.start_y = Signal(signed(16))
        self.incxy   = Signal(signed(16))
        self.incyy   = Signal(signed(16))
        self.rombase = Signal(16)
        self.mode    = Signal(16)

        self.xbp = Signal(24)
        self.ybp = Signal(24)
        self.xcp = Signal(24)
        self.ycp = Signal(24)
        self.pnhsy = Signal(reset = 1)
        self.pnhbk = Signal(reset = 1)
        self.pnvsy = Signal(reset = 1)
        self.pnvbk = Signal(reset = 1)

        self.in_read = Signal()
        self.xy_hold = Signal(9)


    def elaborate(self, platform):
        m = Module()

        vraml = Memory(width = 8, depth = 0x400, name='vraml')
        vramh = Memory(width = 8, depth = 0x400, name='vramh')
        m.submodules.rdportl = rdportl = vraml.read_port(domain = 'sync', transparent = False)
        m.submodules.rdporth = rdporth = vramh.read_port(domain = 'sync', transparent = False)
        m.submodules.wrportl = wrportl = vraml.write_port(domain = 'sync')
        m.submodules.wrporth = wrporth = vramh.write_port(domain = 'sync')

        m.d.comb += self.o_xcp.eq(self.xcp)
        m.d.comb += self.o_ycp.eq(self.ycp)
        m.d.comb += self.o_vramadr.eq(rdportl.addr)
        m.d.comb += self.o_vramen.eq(rdportl.en)
        m.d.comb += self.o_rdata[:8].eq(rdportl.data)
        m.d.comb += self.o_rdata[8:].eq(rdporth.data)
        m.d.comb += self.o_start_x.eq(self.start_x)
        m.d.comb += self.o_incxx.eq(self.incxx)

        # vram write
        with m.If(self.i_p6m):
            with m.If(~self.i_vrcs & ~self.i_rw):
                with m.If(self.i_ab[10]):
                    m.d.sync += [ wrporth.data.eq(self.i_db), wrporth.addr.eq(self.i_ab[:10]), wrporth.en.eq(1) ]
                with m.Else():
                    m.d.sync += [ wrportl.data.eq(self.i_db), wrportl.addr.eq(self.i_ab[:10]), wrportl.en.eq(1) ]
        with m.Else():
            m.d.sync += [ wrporth.en.eq(0), wrportl.en.eq(0) ]

        # vram read
        with m.If(~self.i_vrcs & self.i_rw):
            with m.If(self.i_n6m):
                with m.If(self.i_ab[10]):
                    m.d.sync += [ rdporth.addr.eq(self.i_ab[:10]), rdporth.en.eq(1), self.in_read.eq(1) ]
                    with m.If(self.in_read):
                        m.d.sync += self.o_db.eq(rdporth.data)
                with m.Else():
                    m.d.sync += [ rdportl.addr.eq(self.i_ab[:10]), rdportl.en.eq(1), self.in_read.eq(1) ]
                    with m.If(self.in_read):
                        m.d.sync += self.o_db.eq(rdportl.data)
        with m.If(self.i_n6m & (self.i_vrcs | ~self.i_rw)):
            m.d.sync += self.o_db.eq(0xff)
            m.d.sync += [ rdporth.en.eq(0), rdportl.en.eq(0), self.in_read.eq(0) ]

        # register write
        with m.If(self.i_p6m):
            with m.If((~self.i_iocs) & (~self.i_rw)):
                 with m.Switch(self.i_ab):
                     with m.Case(0x0):
                         m.d.sync += self.start_x[8:].eq(self.i_db)
                     with m.Case(0x1):
                         m.d.sync += self.start_x[:8].eq(self.i_db)
                     with m.Case(0x2):
                         m.d.sync += self.incxx[8:].eq(self.i_db)
                     with m.Case(0x3):
                         m.d.sync += self.incxx[:8].eq(self.i_db)
                     with m.Case(0x4):
                         m.d.sync += self.incyx[8:].eq(self.i_db)
                     with m.Case(0x5):
                         m.d.sync += self.incyx[:8].eq(self.i_db)
                     with m.Case(0x6):
                         m.d.sync += self.start_y[8:].eq(self.i_db)
                     with m.Case(0x7):
                         m.d.sync += self.start_y[:8].eq(self.i_db)
                     with m.Case(0x8):
                         m.d.sync += self.incxy[8:].eq(self.i_db)
                     with m.Case(0x9):
                         m.d.sync += self.incxy[:8].eq(self.i_db)
                     with m.Case(0xa):
                         m.d.sync += self.incyy[8:].eq(self.i_db)
                     with m.Case(0xb):
                         m.d.sync += self.incyy[:8].eq(self.i_db)
                     with m.Case(0xc):
                         m.d.sync += self.rombase[8:].eq(self.i_db)
                     with m.Case(0xd):
                         m.d.sync += self.rombase[:8].eq(self.i_db)
                     with m.Case(0xe):
                         m.d.sync += self.mode.eq(self.i_db)
        
        # ROZ generation
        with m.If(self.i_n6m):
             m.d.sync += self.pnhsy.eq(self.i_nhsy)
             m.d.sync += self.pnhbk.eq(self.i_nhbk)

             cx = Signal(24)
             cy = Signal(24)

             with m.If((~self.pnhbk) & self.i_nhbk):
                 m.d.sync += self.pnvsy.eq(self.i_nvsy)
                 m.d.sync += self.pnvbk.eq(self.i_nvbk)
                 with m.If((~self.pnvbk) & self.i_nvbk):
                     m.d.comb += cx[8:].eq(self.start_x + self.incxx[8:])
                     m.d.comb += cy[8:].eq(self.start_y + self.incxy[8:])
                     m.d.comb += cx[:8].eq(self.incxx[:8])
                     m.d.comb += cy[:8].eq(self.incxy[:8])
                     m.d.sync += self.xbp.eq(cx)
                     m.d.sync += self.ybp.eq(cy)
                 with m.Else():
                     m.d.comb += cx.eq(self.xbp + self.incyx)
                     m.d.comb += cy.eq(self.ybp + self.incyy)
                     m.d.sync += self.xbp.eq(cx)
                     m.d.sync += self.ybp.eq(cy)
             with m.Else():
                 m.d.comb += cx.eq(self.xcp + self.incxx)
                 m.d.comb += cy.eq(self.ycp + self.incxy)

             m.d.sync += self.xcp.eq(cx)
             m.d.sync += self.ycp.eq(cy)

             vramadr = Signal(10)
             m.d.comb += vramadr[:5].eq(self.xcp[15:20])
             m.d.comb += vramadr[5:].eq(self.ycp[15:20])
             m.d.sync += [ rdportl.addr.eq(vramadr), rdportl.en.eq(1) ]
             m.d.sync += [ rdporth.addr.eq(vramadr), rdporth.en.eq(1) ]

             m.d.sync += self.xy_hold[0:4].eq(self.xcp[11:15])
             m.d.sync += self.xy_hold[4:8].eq(self.ycp[11:15])
             m.d.sync += self.xy_hold[  8].eq((self.xcp[20:] != 0) | (self.ycp[20:] != 0))
             m.d.sync += self.o_ca[ 0: 8].eq(self.xy_hold[:8])
             m.d.sync += self.o_ca[ 8:16].eq(rdportl.data)
             m.d.sync += self.o_ca[16:24].eq(rdporth.data)
             m.d.sync += self.o_oblk.eq(self.xy_hold[8] & 0)

        return m
