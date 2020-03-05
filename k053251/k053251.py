from nmigen import *

class k053251(Elaboratable):
    def __init__(self):
        self.i_pclk  = Signal()
        self.i_ab    = Signal(4)
        self.i_db    = Signal(6)
        self.i_cs    = Signal()

        self.i_sdi   = Signal(2)
        self.i_pr0   = Signal(6)
        self.i_pr1   = Signal(6)
        self.i_pr2   = Signal(6)
        self.i_ci0   = Signal(9)
        self.i_ci1   = Signal(9)
        self.i_ci2   = Signal(9)
        self.i_ci3   = Signal(8)
        self.i_ci4   = Signal(8)

        self.o_c0    = Signal(11)
        self.o_sd0   = Signal(2)
        self.o_ncol  = Signal()
        self.o_brit  = Signal()

        self.pri0    = Signal(6)
        self.pri1    = Signal(6)
        self.pri2    = Signal(6)
        self.pri3    = Signal(6)
        self.pri4    = Signal(6)
        self.sha0pri = Signal(6)
        self.sha1pri = Signal(6)
        self.unk7    = Signal(6)
        self.unk8    = Signal(6)
        self.cblk012 = Signal(6)
        self.cblk34  = Signal(6)
        self.unkb    = Signal(6)
        self.inpri   = Signal(3)
        self.extsha  = Signal(6)

        self.c0_1    = Signal(11)
        self.c0_2    = Signal(11)
        self.c0_3    = Signal(11)
        self.c0_4    = Signal(11)
        self.ncol_1  = Signal()
        self.ncol_2  = Signal()
        self.ncol_3  = Signal()
        self.ncol_4  = Signal()
        self.pri_1   = Signal(6)
        self.pri_2   = Signal(6)
        self.pri_3   = Signal(6)
        self.pri_4   = Signal(6)
        self.l1c1    = Signal(11)
        self.l1p1    = Signal(6)
        self.l2c1    = Signal(11)
        self.l2p1    = Signal(6)
        self.l2c2    = Signal(11)
        self.l2p2    = Signal(6)
        self.l3c1    = Signal(11)
        self.l3p1    = Signal(6)
        self.l3c2    = Signal(11)
        self.l3p2    = Signal(6)
        self.l3c3    = Signal(11)
        self.l3p3    = Signal(6)
        self.l4c1    = Signal(11)
        self.l4p1    = Signal(6)
        self.l4c2    = Signal(11)
        self.l4p2    = Signal(6)
        self.l4c3    = Signal(11)
        self.l4p3    = Signal(6)
        self.l4c4    = Signal(11)
        self.l4p4    = Signal(6)
        
    def elaborate(self, platform):
        m = Module()

        with m.If(self.i_pclk):
            l0pri = Signal(6)
            with m.If(self.inpri[0]):
                m.d.comb += l0pri.eq(self.pri0)
            with m.Else():
                m.d.comb += l0pri.eq(self.i_pr0)
            with m.If(self.i_ci0[:4] != 0):
                m.d.sync += self.ncol_1.eq(0)
            with m.Else():
                m.d.sync += self.ncol_1.eq(1)
            m.d.sync += self.pri_1.eq(l0pri)
            m.d.sync += self.c0_1[:9].eq(self.i_ci0)
            m.d.sync += self.c0_1[9:].eq(self.cblk012[0:2])

            l1pri = Signal(6)
            with m.If(self.inpri[1]):
                m.d.comb += l1pri.eq(self.pri1)
            with m.Else():
                m.d.comb += l1pri.eq(self.i_pr1)
                
            m.d.sync += self.l1c1[:9].eq(self.i_ci1)
            m.d.sync += self.l1c1[9:].eq(self.cblk012[2:4])
            m.d.sync += self.l1p1.eq(l1pri)
            with m.If((self.l1c1[:4] != 0) & (self.ncol_1 | (self.l1p1 < self.pri_1))):
                m.d.sync += self.ncol_2.eq(0)
                m.d.sync += self.pri_2.eq(self.l1p1)
                m.d.sync += self.c0_2.eq(self.l1c1)
            with m.Else():
                m.d.sync += self.ncol_2.eq(self.ncol_1)
                m.d.sync += self.pri_2.eq(self.pri_1)
                m.d.sync += self.c0_2.eq(self.c0_1)
            
            l2pri = Signal(6)
            with m.If(self.inpri[2]):
                m.d.comb += l2pri.eq(self.pri2)
            with m.Else():
                m.d.comb += l2pri.eq(self.i_pr2)

            m.d.sync += self.l2c1[:9].eq(self.i_ci2)
            m.d.sync += self.l2c1[9:].eq(self.cblk012[4:6])
            m.d.sync += self.l2p1.eq(l2pri)
            m.d.sync += self.l2c2.eq(self.l2c1)
            m.d.sync += self.l2p2.eq(self.l2p1)
            with m.If((self.l2c2[:4] != 0) & (self.ncol_2 | (self.l2p2 < self.pri_2))):
                m.d.sync += self.ncol_3.eq(0)
                m.d.sync += self.pri_3.eq(self.l2p2)
                m.d.sync += self.c0_3.eq(self.l2c2)
            with m.Else():
                m.d.sync += self.ncol_3.eq(self.ncol_2)
                m.d.sync += self.pri_3.eq(self.pri_2)
                m.d.sync += self.c0_3.eq(self.c0_2)

            m.d.sync += self.l3c1[:8].eq(self.i_ci3)
            m.d.sync += self.l3c1[8:].eq(self.cblk34[0:3])
            m.d.sync += self.l3p1.eq(self.pri3)
            m.d.sync += self.l3c2.eq(self.l3c1)
            m.d.sync += self.l3p2.eq(self.l3p1)
            m.d.sync += self.l3c3.eq(self.l3c2)
            m.d.sync += self.l3p3.eq(self.l3p2)
            with m.If((self.l3c3[:4] != 0) & (self.ncol_3 | (self.l3p3 < self.pri_3))):
                m.d.sync += self.ncol_4.eq(0)
                m.d.sync += self.pri_4.eq(self.l3p3)
                m.d.sync += self.c0_4.eq(self.l3c3)
            with m.Else():
                m.d.sync += self.ncol_4.eq(self.ncol_3)
                m.d.sync += self.pri_4.eq(self.pri_3)
                m.d.sync += self.c0_4.eq(self.c0_3)

            m.d.sync += self.l4c1[:8].eq(self.i_ci4)
            m.d.sync += self.l4c1[8:].eq(self.cblk34[4:6])
            m.d.sync += self.l4p1.eq(self.pri4)
            m.d.sync += self.l4c2.eq(self.l4c1)
            m.d.sync += self.l4p2.eq(self.l4p1)
            m.d.sync += self.l4c3.eq(self.l4c2)
            m.d.sync += self.l4p3.eq(self.l4p2)
            m.d.sync += self.l4c4.eq(self.l4c3)
            m.d.sync += self.l4p4.eq(self.l4p3)
            with m.If((self.l4c4[:4] != 0) & (self.ncol_4 | (self.l4p4 < self.pri_4))):
                m.d.sync += self.o_ncol.eq(0)
                m.d.sync += self.o_c0.eq(self.l4c4)
            with m.Else():
                m.d.sync += self.o_ncol.eq(self.ncol_4)
                m.d.sync += self.o_c0.eq(self.c0_4)


            with m.If(~self.i_cs):
                with m.Switch(self.i_ab):
                    with m.Case(0x0):
                         m.d.sync += self.pri0.eq(self.i_db)
                    with m.Case(0x1):
                         m.d.sync += self.pri1.eq(self.i_db)
                    with m.Case(0x2):
                         m.d.sync += self.pri2.eq(self.i_db)
                    with m.Case(0x3):
                         m.d.sync += self.pri3.eq(self.i_db)
                    with m.Case(0x4):
                         m.d.sync += self.pri4.eq(self.i_db)
                    with m.Case(0x5):
                         m.d.sync += self.sha0pri.eq(self.i_db)
                    with m.Case(0x6):
                         m.d.sync += self.sha1pri.eq(self.i_db)
                    with m.Case(0x7):
                         m.d.sync += self.unk7.eq(self.i_db)
                    with m.Case(0x8):
                         m.d.sync += self.unk8.eq(self.i_db)
                    with m.Case(0x9):
                         m.d.sync += self.cblk012.eq(self.i_db)
                    with m.Case(0xa):
                         m.d.sync += self.cblk34.eq(self.i_db)
                    with m.Case(0xb):
                         m.d.sync += self.unkb.eq(self.i_db)
                    with m.Case(0xc):
                         m.d.sync += self.inpri.eq(self.i_db)
                    with m.Case(0xd):
                         m.d.sync += self.extsha.eq(self.i_db)

        return m
