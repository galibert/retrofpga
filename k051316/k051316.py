from nmigen import *

class k051316(Elaboratable):
    def __init__(self, defram, r):
        self.i_ab = Signal(11)
        self.i_db = Signal(8)
        self.i_vrcs = Signal()
        self.i_iocs = Signal()
        self.i_rw = Signal()
        self.i_clk2 = Signal()
        self.i_nhsy = Signal()
        self.i_nhbk = Signal()
        self.i_nvsy = Signal()
        self.i_nvbk = Signal()

        self.o_ca = Signal(24)
        self.o_oblk = Signal()

        self.o_vramadr = Signal(10)
        self.o_rdata = Signal(16)
        self.o_xcp = Signal(24)
        self.o_ycp = Signal(24)

        self.start_x = Signal(signed(16), reset = r[0])
        self.incxx   = Signal(signed(16), reset = r[1])
        self.incyx   = Signal(signed(16), reset = r[2])
        self.start_y = Signal(signed(16), reset = r[3])
        self.incxy   = Signal(signed(16), reset = r[4])
        self.incyy   = Signal(signed(16), reset = r[5])
        self.rombase = Signal(16, reset = r[6])
        self.mode    = Signal(16, reset = r[7])

        self.xbp = Signal(24)
        self.ybp = Signal(24)
        self.xcp = Signal(24)
        self.ycp = Signal(24)
        self.pnhsy = Signal(reset = 1)
        self.pnhbk = Signal(reset = 1)
        self.pnvsy = Signal(reset = 1)
        self.pnvbk = Signal(reset = 1)

        irawdata = open(defram, 'rb').read()
        idatal = []
        idatah = []
        for i in range(0, 0x400):
            idatal.append(irawdata[i*2])
            idatah.append(irawdata[i*2+0x800])

        self.vraml = Memory(width = 8, depth = 0x400, init = idatal)
        self.vramh = Memory(width = 8, depth = 0x400, init = idatah)

    def elaborate(self, platform):
        m = Module()
        m.submodules.rdportl = rdportl = self.vraml.read_port(domain = 'sync')
        m.submodules.rdporth = rdporth = self.vramh.read_port(domain = 'sync')

        m.d.comb += self.o_xcp.eq(self.xcp)
        m.d.comb += self.o_ycp.eq(self.ycp)
        m.d.comb += self.o_vramadr.eq(rdportl.addr)
        m.d.comb += self.o_rdata[:8].eq(rdportl.data)
        m.d.comb += self.o_rdata[8:].eq(rdporth.data)

        with m.If(self.i_clk2):
            m.d.sync += self.pnhsy.eq(self.i_nhsy)
            m.d.sync += self.pnhbk.eq(self.i_nhbk)

            cx = Signal(24)
            cy = Signal(24)

            with m.If((~self.pnhsy) & self.i_nhsy):
                m.d.sync += self.pnvsy.eq(self.i_nvsy)
                m.d.sync += self.pnvbk.eq(self.i_nvbk)
                with m.If((~self.pnvsy) & self.i_nvsy):
                    m.d.comb += cx[8:].eq(self.start_x)
                    m.d.comb += cy[8:].eq(self.start_y)
                    m.d.comb += cx[:8].eq(0)
                    m.d.comb += cy[:8].eq(0)
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

            m.d.comb += rdportl.addr.eq(0x155)
            m.d.comb += rdporth.addr.eq(0x155)

            m.d.sync += self.o_ca[ 0: 4].eq(self.xcp[11:15])
            m.d.sync += self.o_ca[ 4: 8].eq(self.ycp[11:15])
            m.d.sync += self.o_ca[ 8:16].eq(rdportl.data)
            m.d.sync += self.o_ca[16:24].eq(rdporth.data)
            m.d.sync += self.o_oblk.eq((self.xcp[20:] != 0) | (self.ycp[20:] != 0))

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
        with m.Else():
            vramadr = Signal(10)
            m.d.comb += vramadr[:5].eq(self.xcp[15:20])
            m.d.comb += vramadr[5:].eq(self.ycp[15:20])
            m.d.comb += rdportl.addr.eq(vramadr)
            m.d.comb += rdporth.addr.eq(vramadr)

        return m

