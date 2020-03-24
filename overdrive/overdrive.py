import sys
sys.path.append('..')

from k053252 import k053252
from k051316 import k051316
from k053251 import k053251
from nmigen import *

def rom_load_bytes(fname):
    rawdata = open(fname, 'rb').read()
    r = []
    for i in range(0, len(rawdata)):
        r.append(rawdata[i])
    return r

def rom_load_bytes_swap(fname):
    rawdata = open(fname, 'rb').read()
    r = []
    for i in range(0, len(rawdata)):
        r.append(rawdata[i^1])
    return r

class overdrive(Elaboratable):
    def __init__(self):
        self.i_ab1    = Signal(23)
        self.i_db1    = Signal(16)
        self.o_db1    = Signal(16)
        self.i_uds1   = Signal()
        self.i_lds1   = Signal()
        self.i_as1    = Signal()
        self.i_rw1    = Signal()
        self.o_dtack1 = Signal()

        self.i_ab2    = Signal(23)
        self.i_db2    = Signal(16)
        self.o_db2    = Signal(16)
        self.i_uds2   = Signal()
        self.i_lds2   = Signal()
        self.i_as2    = Signal()
        self.i_rw2    = Signal()
        self.o_dtack2 = Signal()

        self.o_nhsy = Signal()
        self.o_nhbk = Signal()
        self.o_nvsy = Signal()
        self.o_nvbk = Signal()
        self.o_c0   = Signal(11)

        self.o_p12m = Signal()
        self.o_n12m = Signal()
        self.o_p6m  = Signal()
        self.o_n6m  = Signal()
        self.o_p6md = Signal()
        self.o_n6md = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.timings = timings = k053252.k053252()
        m.submodules.roz_1   = roz_1   = k051316.k051316()
        m.submodules.roz_2   = roz_2   = k051316.k051316()
        m.submodules.mixer   = mixer   = k053251.k053251()

        m.submodules.roz1rd = roz1rd = Memory(width = 8, depth = 0x20000, init = rom_load_bytes("roms/789e06.a21")).read_port()
        m.submodules.roz2rd = roz2rd = Memory(width = 8, depth = 0x20000, init = rom_load_bytes("roms/789e07.c23")).read_port()

        # Address decoder 1
        rom1cs   = Signal()
        ram1cs   = Signal()
        cramcs   = Signal()
        ccucs    = Signal()
        afr      = Signal()
        adccs    = Signal()
        swrd     = Signal()
        radiosw  = Signal()
        mdcs1    = Signal()
        mdcs2    = Signal()
        psacset1 = Signal()
        psacset2 = Signal()
        pcucs    = Signal()
        soundcs1 = Signal()
        soundcs2 = Signal()
        soundon  = Signal()
        wrport1  = Signal()
        wrport2  = Signal()
        hcomcs   = Signal()
        psac1cs  = Signal()
        psac2cs  = Signal()
        psaccha1 = Signal()
        psaccha2 = Signal()
        hostint1 = Signal()
        hostint2 = Signal()

        rom21cs  = Signal()
        rom22cs  = Signal()
        ram2cs   = Signal()
        lvccs    = Signal()
        lvcset1  = Signal()
        lvcset2  = Signal()
        crtint   = Signal()
        objcs    = Signal()
        objcha   = Signal()
        syswra   = Signal()
        objset   = Signal()
        alustart = Signal()
        acomcs   = Signal()
        aluwkcs  = Signal()
        lvccha1  = Signal()
        lvccha2  = Signal()

        m.d.comb += rom1cs.eq(   ~((self.i_ab1[18-1:22-1] == 0x00) & (self.i_as1 == 0)))
        m.d.comb += ram1cs.eq(   ~((self.i_ab1[18-1:22-1] == 0x01) & (self.i_as1 == 0)))
        m.d.comb += cramcs.eq(   ~((self.i_ab1[18-1:22-1] == 0x02) & (self.i_as1 == 0)))
        m.d.comb += swrd.eq(     ~((self.i_ab1[16-1:22-1] == 0x0c) & (self.i_as1 == 0)))
        m.d.comb += radiosw.eq(  ~((self.i_ab1[16-1:22-1] == 0x0d) & (self.i_as1 == 0)))
        m.d.comb += mdcs1.eq(    ~((self.i_ab1[16-1:22-1] == 0x0e) & (self.i_as1 == 0)))
        m.d.comb += mdcs2.eq(    ~((self.i_ab1[16-1:22-1] == 0x0f) & (self.i_as1 == 0)))
        m.d.comb += ccucs.eq(    ~((self.i_ab1[18-1:22-1] == 0x04) & (self.i_as1 == 0)))
        m.d.comb += afr.eq(      ~((self.i_ab1[18-1:22-1] == 0x05) & (self.i_as1 == 0)))
        m.d.comb += adccs.eq(    ~((self.i_ab1[18-1:22-1] == 0x06) & (self.i_as1 == 0)))
        m.d.comb += psacset1.eq( ~((self.i_ab1[15-1:22-1] == 0x38) & (self.i_as1 == 0)))
        m.d.comb += psacset2.eq( ~((self.i_ab1[15-1:22-1] == 0x39) & (self.i_as1 == 0)))
        m.d.comb += pcucs.eq(    ~((self.i_ab1[15-1:22-1] == 0x3a) & (self.i_as1 == 0)))
        m.d.comb += soundcs1.eq( ~((self.i_ab1[15-1:22-1] == 0x3b) & (self.i_as1 == 0)))
        m.d.comb += soundcs2.eq( ~((self.i_ab1[15-1:22-1] == 0x3c) & (self.i_as1 == 0)))
        m.d.comb += soundon.eq(  ~((self.i_ab1[15-1:22-1] == 0x3d) & (self.i_as1 == 0)))
        m.d.comb += wrport1.eq(  ~((self.i_ab1[15-1:22-1] == 0x3e) & (self.i_as1 == 0)))
        m.d.comb += wrport2.eq(  ~((self.i_ab1[15-1:22-1] == 0x3f) & (self.i_as1 == 0)))
        m.d.comb += hcomcs.eq(   ~((self.i_ab1[15-1:18-1] ==  0x0) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += psac1cs.eq(  ~((self.i_ab1[15-1:18-1] ==  0x2) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += psac2cs.eq(  ~((self.i_ab1[15-1:18-1] ==  0x3) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += psaccha1.eq( ~((self.i_ab1[15-1:18-1] ==  0x4) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += psaccha2.eq( ~((self.i_ab1[15-1:18-1] ==  0x5) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += hostint1.eq( ~((self.i_ab1[15-1:18-1] ==  0x6) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))
        m.d.comb += hostint2.eq( ~((self.i_ab1[15-1:18-1] ==  0x7) & (self.i_ab1[21-1] == 1) & (self.i_ab1[23-1] == 0) & (self.i_as1 == 0)))

        m.d.comb += rom21cs.eq(  ~((self.i_ab2[18-1:22-1] == 0x00) & (self.i_as2 == 0)))
        m.d.comb += rom22cs.eq(  ~((self.i_ab2[18-1:22-1] == 0x01) & (self.i_as2 == 0)))
        m.d.comb += ram2cs.eq(   ~((self.i_ab2[18-1:22-1] == 0x02) & (self.i_as2 == 0)))
        m.d.comb += lvccs.eq(    ~((self.i_ab2[18-1:22-1] == 0x03) & (self.i_as2 == 0)))
        m.d.comb += lvcset1.eq(  ~((self.i_ab2[15-1:22-1] == 0x20) & (self.i_as2 == 0)))
        m.d.comb += lvcset2.eq(  ~((self.i_ab2[15-1:22-1] == 0x21) & (self.i_as2 == 0)))
        m.d.comb += crtint.eq(   ~((self.i_ab2[15-1:22-1] == 0x22) & (self.i_as2 == 0)))
        m.d.comb += objcs.eq(    ~((self.i_ab2[15-1:22-1] == 0x23) & (self.i_as2 == 0)))
        m.d.comb += objcha.eq(   ~((self.i_ab2[15-1:22-1] == 0x24) & (self.i_as2 == 0)))
        m.d.comb += syswra.eq(   ~((self.i_ab2[15-1:22-1] == 0x25) & (self.i_as2 == 0)))
        m.d.comb += objset.eq(   ~((self.i_ab2[15-1:22-1] == 0x26) & (self.i_as2 == 0)))
        m.d.comb += alustart.eq( ~((self.i_ab2[18-1:22-1] == 0x05) & (self.i_as2 == 0)))
        m.d.comb += acomcs.eq(   ~((self.i_ab2[15-1:18-1] ==  0x0) & (self.i_ab2[21-1] == 1) & (self.i_ab2[23-1] == 0) & (self.i_as2 == 0)))
        m.d.comb += aluwkcs.eq(  ~((self.i_ab2[15-1:18-1] ==  0x1) & (self.i_ab2[21-1] == 1) & (self.i_ab2[23-1] == 0) & (self.i_as2 == 0)))
        m.d.comb += lvccha1.eq(  ~((self.i_ab2[15-1:18-1] ==  0x3) & (self.i_ab2[21-1] == 1) & (self.i_ab2[23-1] == 0) & (self.i_as2 == 0)))
        m.d.comb += lvccha2.eq(  ~((self.i_ab2[15-1:18-1] ==  0x4) & (self.i_ab2[21-1] == 1) & (self.i_ab2[23-1] == 0) & (self.i_as2 == 0)))
        
        # dtack 1
        hcomdtk  = Signal(reset = 1)
        psacdtk  = Signal(reset = 1)
        m.d.comb += self.o_dtack1.eq(hcomdtk & hostint1 & hostint2 & psacdtk & (self.i_as1 | self.i_ab1[21-1]))

        # data bus collection 1
        m.d.comb += self.o_db1[0:8].eq(timings.o_db)
        m.d.comb += self.o_db1[8:16].eq(roz_1.o_db & roz_2.o_db)

        # dtack 2
        acomdtk  = Signal(reset = 1)
        aluwkdtk = Signal(reset = 1)
        lvcchad1 = Signal(reset = 1)
        lvcchad2 = Signal(reset = 1)

        with m.If(self.i_as2):
            m.d.sync += lvcchad1.eq(1)
            m.d.sync += lvcchad2.eq(1)
        with m.Elif(timings.o_clk2n):
            m.d.sync += lvcchad1.eq(lvccha1 & lvccha2)
            m.d.sync += lvcchad2.eq(lvcchad1)

        m.d.comb += self.o_dtack2.eq(acomdtk & aluwkdtk & (self.i_as1 | self.i_ab1[21-1]) & lvcchad2)


        # Timings hookup
        m.d.comb += timings.i_ab.eq(self.i_ab1[:4])
        m.d.comb += timings.i_db.eq(self.i_db1[0:8])
        m.d.comb += timings.i_rw.eq(self.i_rw1)
        m.d.comb += timings.i_ccs.eq(ccucs)
        m.d.comb += timings.i_clkp.eq(1)
        m.d.comb += self.o_nhsy.eq(timings.o_nhsy)
        m.d.comb += self.o_nvsy.eq(timings.o_nvsy)
        m.d.comb += self.o_nhbk.eq(timings.o_nhbk)
        m.d.comb += self.o_nvbk.eq(timings.o_nvbk)
        m.d.comb += self.o_p12m.eq(timings.o_clk1p)
        m.d.comb += self.o_n12m.eq(timings.o_clk1n)
        m.d.comb += self.o_p6m.eq (timings.o_clk2p)
        m.d.comb += self.o_n6m.eq (timings.o_clk2n)
        m.d.comb += self.o_p6md.eq(timings.o_clk4p)
        m.d.comb += self.o_n6md.eq(timings.o_clk4n)

        # p12m = clk1p
        # n12m = clk1n
        # p6m  = clk2p
        # n6m  = clk2n
        # p6md = clk4p
        # p6md = clk4n

        # General ROZ hookup
        pcs1 = Signal()
        pcs2 = Signal()
        pset1 = Signal()
        pset2 = Signal()
        psac1csd1 = Signal()
        psac1csd2 = Signal()
        psac2csd1 = Signal()
        psac2csd2 = Signal()
        psacchad1 = Signal()
        
        with m.If(self.i_as1):
            m.d.sync += psac1csd1.eq(1)
            m.d.sync += psac1csd2.eq(1)
            m.d.sync += pset1.eq(1)
            m.d.sync += psac2csd1.eq(1)
            m.d.sync += psac2csd2.eq(1)
            m.d.sync += pset2.eq(1)
        with m.Elif(timings.o_clk4n):
            m.d.sync += psac1csd1.eq(psac1cs)
            m.d.sync += psac1csd2.eq(psac1csd1)
            m.d.sync += pset1.eq(psacset1)
            m.d.sync += psac2csd1.eq(psac2cs)
            m.d.sync += psac2csd2.eq(psac2csd1)
            m.d.sync += pset2.eq(psacset2)

        m.d.comb += pcs1.eq(~((~psac1csd1) & (self.i_rw1 | psac1csd2)))
        m.d.comb += pcs2.eq(~((~psac2csd1) & (self.i_rw1 | psac2csd2)))

        with m.If(self.i_as1):
            m.d.sync += psacchad1.eq(1)
            m.d.sync += psacdtk.eq(1)
        with m.Elif(timings.o_clk2n):
            m.d.sync += psacchad1.eq(~(psaccha1 & psaccha2))
            m.d.sync += psacdtk.eq(psacchad1 & psac1csd1 & psac1csd1)
        
        # ROZ1 hookup including rom
        m.d.comb += roz_1.i_vrcs.eq(pcs1)
        m.d.comb += roz_1.i_iocs.eq(pset1)
        m.d.comb += roz_1.i_p12m.eq(timings.o_clk1n)
        m.d.comb += roz_1.i_n12m.eq(timings.o_clk1p)
        m.d.comb += roz_1.i_p6m.eq(timings.o_clk2n)
        m.d.comb += roz_1.i_n6m.eq(timings.o_clk2p)
        with m.If(timings.o_clk2n):
            m.d.sync += roz_1.i_ab.eq(self.i_ab1[:11])
        m.d.comb += roz_1.i_db.eq(self.i_db1[8:])
        m.d.comb += roz_1.i_rw.eq(self.i_rw1)
        with m.If(timings.o_clk2p):
            m.d.sync += roz_1.i_nhsy.eq(timings.o_nhsy)
            m.d.sync += roz_1.i_nhbk.eq(timings.o_nhbk)
            m.d.sync += roz_1.i_nvsy.eq(timings.o_nvsy)
            m.d.sync += roz_1.i_nvbk.eq(timings.o_nvbk)
        m.d.comb += roz1rd.addr.eq(roz_1.o_ca[1:18])
        with m.If(roz_1.o_oblk):
            m.d.comb += mixer.i_ci4[:4].eq(0)
        with m.Elif(roz_1.o_ca[0]):
            m.d.comb += mixer.i_ci4[:4].eq(roz1rd.data[4:])
        with m.Else():
            m.d.comb += mixer.i_ci4[:4].eq(roz1rd.data[:4])
        m.d.comb += mixer.i_ci4[4:].eq(roz_1.o_ca[18:22])

        # ROZ2 hookup including rom
        m.d.comb += roz_2.i_vrcs.eq(pcs2)
        m.d.comb += roz_2.i_iocs.eq(pset2)
        m.d.comb += roz_2.i_p12m.eq(timings.o_clk1n)
        m.d.comb += roz_2.i_n12m.eq(timings.o_clk1p)
        m.d.comb += roz_2.i_p6m.eq(timings.o_clk2n)
        m.d.comb += roz_2.i_n6m.eq(timings.o_clk2p)
        with m.If(timings.o_clk2n):
            m.d.sync += roz_2.i_ab.eq(self.i_ab1[:11])
        m.d.comb += roz_2.i_db.eq(self.i_db1[8:])
        m.d.comb += roz_2.i_rw.eq(self.i_rw1)
        with m.If(timings.o_clk2p):
            m.d.sync += roz_2.i_nhsy.eq(timings.o_nhsy)
            m.d.sync += roz_2.i_nhbk.eq(timings.o_nhbk)
            m.d.sync += roz_2.i_nvsy.eq(timings.o_nvsy)
            m.d.sync += roz_2.i_nvbk.eq(timings.o_nvbk)
        m.d.comb += roz2rd.addr.eq(roz_2.o_ca[1:18])
        with m.If(roz_2.o_oblk):
            m.d.comb += mixer.i_ci3[:4].eq(0)
        with m.Elif(roz_2.o_ca[0]):
            m.d.comb += mixer.i_ci3[:4].eq(roz2rd.data[:4])
        with m.Else():
            m.d.comb += mixer.i_ci3[:4].eq(roz2rd.data[4:])
        m.d.comb += mixer.i_ci3[4:].eq(roz_2.o_ca[18:22])

        # Mixer hookup
        m.d.comb += mixer.i_pclk.eq(timings.o_clk2p)
        m.d.comb += mixer.i_cs.eq(pcucs)
        m.d.comb += mixer.i_ab.eq(self.i_ab1[:4])
        m.d.comb += mixer.i_db.eq(self.i_db1[8:14])
        m.d.comb += mixer.i_sdi[1].eq(0)
        m.d.comb += mixer.i_sdi[0].eq(0)
        m.d.comb += mixer.i_pr0.eq(0x3f)
        m.d.comb += mixer.i_pr1.eq(0x3f)
        m.d.comb += mixer.i_pr2.eq(0x3f)
        m.d.comb += mixer.i_ci0.eq(0)
        m.d.comb += mixer.i_ci1.eq(0)
        m.d.comb += mixer.i_ci2.eq(0)
        m.d.comb += self.o_c0.eq(mixer.o_c0)

        return m
