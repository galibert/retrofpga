from nmigen import *

class idecode(Elaboratable):
    def __init__(self):
        self.i_ird     = Signal(16)

        self.o_ma1     = Signal(10)
        self.o_ma2     = Signal(10)
        self.o_ma3     = Signal(10)
        self.o_linea   = Signal()
        self.o_linef   = Signal()
        self.o_illegal = Signal()
        self.o_priv    = Signal()

    def elaborate(self, platform):
        m = Module()

        ictx = Signal(11)
        m.d.comb += ictx[ 0].eq(self.i_ird.matches("1110------------"))
        m.d.comb += ictx[ 1].eq(self.i_ird.matches("-------100------"))
        m.d.comb += ictx[ 2].eq(self.i_ird.matches("-------110------") | self.i_ird.matches("----01-011------"))
        m.d.comb += ictx[ 3].eq(self.i_ird.matches("----1000-1------"))
        m.d.comb += ictx[ 4].eq(self.i_ird.matches("----111001------"))
        m.d.comb += ictx[ 5].eq(self.i_ird.matches("--00------------"))
        m.d.comb += ictx[ 6].eq(self.i_ird.matches("---0---1--------"))
        m.d.comb += ictx[ 7].eq(self.i_ird.matches("----00-00-------") | self.i_ird.matches("-----0100-------") | self.i_ird.matches("-------100------"))
        m.d.comb += ictx[ 8].eq(self.i_ird.matches("----100000------") | self.i_ird.matches("-------100------"))
        m.d.comb += ictx[ 9].eq(self.i_ird.matches("----100---------"))
        m.d.comb += ictx[10].eq(self.i_ird.matches("011-------------") | self.i_ird.matches("1110------------"))

        with m.Switch(Cat(ictx, self.i_ird)):
            with m.Case("0100111001111--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("11100---11111-1------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("11100---111111-------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("11100---1100---------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1-00---110000--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1-00---111001--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1-00---0--001--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("11101---11-----------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1--1---000001--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1000---101000--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1------1-01111------------0"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1------10-1111------------0"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1------1-011101-----------0"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1------10-11101-----------0"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("1000------001------------0-"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0111---1-------------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0101------1111-------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0101------111-1------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0101----00001--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100---111-00--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010011-01--00--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100100001100--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010011101-011--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100---111011--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010010001-011--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("01001000-1011--------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010011100111-100-----------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100---10------------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100------111100--------0--"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("01000--01011101------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100-0-01-11101------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100----0-11101--------0---"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100------001---------0----"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010011000------------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("010011-000-----------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0100001011-----------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("00---1-111-----------0-----"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("00--1--111-----------0-----"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0001---001-----------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("000-------001-------0------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0000------111100---0-------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0000------11101---0--------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("00001110-------------------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("0000---011-------0---------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("----------11111-0----------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Case("----------1111-10----------"):
                m.d.comb += self.o_illegal.eq(1)
            with m.Default():
                m.d.comb += self.o_illegal.eq(0)

        with m.Switch(self.i_ird):
            with m.Case("0100011011------"):
                m.d.comb += self.o_priv.eq(1)
            with m.Case("01001110011100-0"):
                m.d.comb += self.o_priv.eq(1)
            with m.Case("010011100111001-"):
                m.d.comb += self.o_priv.eq(1)
            with m.Case("0000-0-001111100"):
                m.d.comb += self.o_priv.eq(1)
            with m.Case("010011100110----"):
                m.d.comb += self.o_priv.eq(1)
            with m.Default():
                m.d.comb += self.o_priv.eq(0)

        bw = Signal()
        with m.Switch(self.i_ird):
            with m.Case('11100---11------'):
                m.d.comb += bw.eq(1)
            with m.Case('0101-----1------'):
                m.d.comb += bw.eq(1)
            with m.Case('0101----0-------'):
                m.d.comb += bw.eq(1)
            with m.Case('1--1---0-1------'):
                m.d.comb += bw.eq(1)
            with m.Case('1--1----0-------'):
                m.d.comb += bw.eq(1)
            with m.Case('1-00-----1------'):
                m.d.comb += bw.eq(1)
            with m.Case('1-00----0-------'):
                m.d.comb += bw.eq(1)
            with m.Case('01001010-1------'):
                m.d.comb += bw.eq(1)
            with m.Case('01000--0-1------'):
                m.d.comb += bw.eq(1)
            with m.Case('0100---000------'):
                m.d.comb += bw.eq(1)
            with m.Case('0100---110------'):
                m.d.comb += bw.eq(1)
            with m.Case('00-1------------'):
                m.d.comb += bw.eq(1)
            with m.Case('0000---1--------'):
                m.d.comb += bw.eq(1)
            with m.Default():
                m.d.comb += bw.eq(0)

        l = Signal()
        with m.Switch(self.i_ird):
            with m.Case('1--1---11-------'):
                m.d.comb += l.eq(1)
            with m.Case('1--1----10------'):
                m.d.comb += l.eq(1)
            with m.Case('1-0-----10------'):
                m.d.comb += l.eq(1)
            with m.Case('0101----10------'):
                m.d.comb += l.eq(1)
            with m.Case('0100101010------'):
                m.d.comb += l.eq(1)
            with m.Case('01000--010------'):
                m.d.comb += l.eq(1)
            with m.Case('0010------------'):
                m.d.comb += l.eq(1)
            with m.Default():
                m.d.comb += l.eq(0)

        m.d.comb += self.o_linea.eq(self.i_ird[12:16] == 0xa)
        m.d.comb += self.o_linef.eq(self.i_ird[12:16] == 0xf)

        m.d.comb += self.o_ma1.eq(0x3ff)
        with m.Switch(Cat(l, bw, self.i_ird)):
            with m.Case('000010001---------'):
                m.d.comb += self.o_ma1.eq(0x2b9)
            with m.Case('0110000100000000--'):
                m.d.comb += self.o_ma1.eq(0x0a9)
            with m.Case('01100001----------'):
                m.d.comb += self.o_ma1.eq(0x089)
            with m.Case('0110----00000000--'):
                m.d.comb += self.o_ma1.eq(0x068)
            with m.Case('0110--------------'):
                m.d.comb += self.o_ma1.eq(0x308)
            with m.Case('0000---010--------'):
                m.d.comb += self.o_ma1.eq(0x3e0)
            with m.Case('0100111001110000--'):
                m.d.comb += self.o_ma1.eq(0x3a6)
            with m.Case('0100100001000-----'):
                m.d.comb += self.o_ma1.eq(0x341)
            with m.Case('0100111001101-----'):
                m.d.comb += self.o_ma1.eq(0x230)
            with m.Case('0100000011000-----'):
                m.d.comb += self.o_ma1.eq(0x3a5)
            with m.Case('0100111001110010--'):
                m.d.comb += self.o_ma1.eq(0x3a2)
            with m.Case('010010001-110-----'):
                m.d.comb += self.o_ma1.eq(0x325)
            with m.Case('010010001-010-----'):
                m.d.comb += self.o_ma1.eq(0x3a0)
            with m.Case('010010001-101-----'):
                m.d.comb += self.o_ma1.eq(0x1f1)
            with m.Case('1110----0-1-------'):
                m.d.comb += self.o_ma1.eq(0x382)
            with m.Case('1110----101-------'):
                m.d.comb += self.o_ma1.eq(0x386)
            with m.Case('1110----0-0-------'):
                m.d.comb += self.o_ma1.eq(0x381)
            with m.Case('1110----100-------'):
                m.d.comb += self.o_ma1.eq(0x385)
            with m.Case('010010001-111000--'):
                m.d.comb += self.o_ma1.eq(0x1ed)
            with m.Case('010010001-111001--'):
                m.d.comb += self.o_ma1.eq(0x1e5)
            with m.Case('0101----11000-----'):
                m.d.comb += self.o_ma1.eq(0x384)
            with m.Case('0100111001110101--'):
                m.d.comb += self.o_ma1.eq(0x126)
            with m.Case('0100111001110-11--'):
                m.d.comb += self.o_ma1.eq(0x12a)
            with m.Case('010001-011000-----'):
                m.d.comb += self.o_ma1.eq(0x301)
            with m.Case('00-1---00000------'):
                m.d.comb += self.o_ma1.eq(0x121)
            with m.Case('0011---00100------'):
                m.d.comb += self.o_ma1.eq(0x279)
            with m.Case('0010---00-00------'):
                m.d.comb += self.o_ma1.eq(0x129)
            with m.Case('1-01---10-000-----'):
                m.d.comb += self.o_ma1.eq(0x1c1)
            with m.Case('1-0----00-00------'):
                m.d.comb += self.o_ma1.eq(0x1c1)
            with m.Case('1-01---01100------'):
                m.d.comb += self.o_ma1.eq(0x1c9)
            with m.Case('1-01---11100------'):
                m.d.comb += self.o_ma1.eq(0x1c5)
            with m.Case('1-01---11-000-----'):
                m.d.comb += self.o_ma1.eq(0x1c5)
            with m.Case('1-0----01000------'):
                m.d.comb += self.o_ma1.eq(0x1c5)
            with m.Case('1011---10-000-----'):
                m.d.comb += self.o_ma1.eq(0x100)
            with m.Case('1011---110000-----'):
                m.d.comb += self.o_ma1.eq(0x10c)
            with m.Case('00-1---11000------'):
                m.d.comb += self.o_ma1.eq(0x1eb)
            with m.Case('0010---11000------'):
                m.d.comb += self.o_ma1.eq(0x1ef)
            with m.Case('00-1---01000------'):
                m.d.comb += self.o_ma1.eq(0x2fa)
            with m.Case('0010---01000------'):
                m.d.comb += self.o_ma1.eq(0x2f9)
            with m.Case('00-1---10000------'):
                m.d.comb += self.o_ma1.eq(0x2f8)
            with m.Case('0010---10000------'):
                m.d.comb += self.o_ma1.eq(0x2fc)
            with m.Case('00-1---01100------'):
                m.d.comb += self.o_ma1.eq(0x2fe)
            with m.Case('0010---01100------'):
                m.d.comb += self.o_ma1.eq(0x2fd)
            with m.Case('00-1---10100------'):
                m.d.comb += self.o_ma1.eq(0x2da)
            with m.Case('0010---10100------'):
                m.d.comb += self.o_ma1.eq(0x2de)
            with m.Case('0111---0----------'):
                m.d.comb += self.o_ma1.eq(0x23b)
            with m.Case('1-00---100000-----'):
                m.d.comb += self.o_ma1.eq(0x1cd)
            with m.Case('00-100011100------'):
                m.d.comb += self.o_ma1.eq(0x2d9)
            with m.Case('001000011100------'):
                m.d.comb += self.o_ma1.eq(0x2dd)
            with m.Case('0101----0-000-----'):
                m.d.comb += self.o_ma1.eq(0x2d8)
            with m.Case('0101----01001-----'):
                m.d.comb += self.o_ma1.eq(0x2dc)
            with m.Case('0101----1000------'):
                m.d.comb += self.o_ma1.eq(0x2dc)
            with m.Case('00-100111100------'):
                m.d.comb += self.o_ma1.eq(0x1ea)
            with m.Case('001000111100------'):
                m.d.comb += self.o_ma1.eq(0x1ee)
            with m.Case('010010001-100-----'):
                m.d.comb += self.o_ma1.eq(0x3a4)
            with m.Case('010011001-011-----'):
                m.d.comb += self.o_ma1.eq(0x123)
            with m.Case('----------011---1-'):
                m.d.comb += self.o_ma1.eq(0x21c)
            with m.Case('----------011----1'):
                m.d.comb += self.o_ma1.eq(0x00f)
            with m.Case('0100100001111011--'):
                m.d.comb += self.o_ma1.eq(0x1ff)
            with m.Case('0100100001110-----'):
                m.d.comb += self.o_ma1.eq(0x1ff)
            with m.Case('0100100001111010--'):
                m.d.comb += self.o_ma1.eq(0x17d)
            with m.Case('0100100001101-----'):
                m.d.comb += self.o_ma1.eq(0x17d)
            with m.Case('0100100001010-----'):
                m.d.comb += self.o_ma1.eq(0x17c)
            with m.Case('----------100---1-'):
                m.d.comb += self.o_ma1.eq(0x103)
            with m.Case('----------100----1'):
                m.d.comb += self.o_ma1.eq(0x179)
            with m.Case('0100100001111000--'):
                m.d.comb += self.o_ma1.eq(0x178)
            with m.Case('0100100001111001--'):
                m.d.comb += self.o_ma1.eq(0x1fa)
            with m.Case('0100111001011-----'):
                m.d.comb += self.o_ma1.eq(0x119)
            with m.Case('0000---00---------'):
                m.d.comb += self.o_ma1.eq(0x2b9)
            with m.Case('010010100-000-----'):
                m.d.comb += self.o_ma1.eq(0x12d)
            with m.Case('0100100010000-----'):
                m.d.comb += self.o_ma1.eq(0x133)
            with m.Case('01000--00-000-----'):
                m.d.comb += self.o_ma1.eq(0x133)
            with m.Case('01000--010000-----'):
                m.d.comb += self.o_ma1.eq(0x137)
            with m.Case('0100100000000-----'):
                m.d.comb += self.o_ma1.eq(0x13b)
            with m.Case('1100----11000-----'):
                m.d.comb += self.o_ma1.eq(0x15b)
            with m.Case('0000---110001-----'):
                m.d.comb += self.o_ma1.eq(0x1ca)
            with m.Case('0000---111001-----'):
                m.d.comb += self.o_ma1.eq(0x1ce)
            with m.Case('0000---100001-----'):
                m.d.comb += self.o_ma1.eq(0x1d2)
            with m.Case('0000---101001-----'):
                m.d.comb += self.o_ma1.eq(0x1d6)
            with m.Case('0100111001100-----'):
                m.d.comb += self.o_ma1.eq(0x2f5)
            with m.Case('010011001-111000--'):
                m.d.comb += self.o_ma1.eq(0x1f9)
            with m.Case('010011001-111001--'):
                m.d.comb += self.o_ma1.eq(0x1e9)
            with m.Case('0100111001010-----'):
                m.d.comb += self.o_ma1.eq(0x30b)
            with m.Case('0100---111111011--'):
                m.d.comb += self.o_ma1.eq(0x1fb)
            with m.Case('0100---111110-----'):
                m.d.comb += self.o_ma1.eq(0x1fb)
            with m.Case('0100---111111010--'):
                m.d.comb += self.o_ma1.eq(0x2f2)
            with m.Case('0100---111101-----'):
                m.d.comb += self.o_ma1.eq(0x2f2)
            with m.Case('0100---111010-----'):
                m.d.comb += self.o_ma1.eq(0x2f1)
            with m.Case('010011001-111011--'):
                m.d.comb += self.o_ma1.eq(0x1f5)
            with m.Case('010011001-110-----'):
                m.d.comb += self.o_ma1.eq(0x1f5)
            with m.Case('010011001-010-----'):
                m.d.comb += self.o_ma1.eq(0x127)
            with m.Case('010011001-111010--'):
                m.d.comb += self.o_ma1.eq(0x1fd)
            with m.Case('010011001-101-----'):
                m.d.comb += self.o_ma1.eq(0x1fd)
            with m.Case('0100---111111000--'):
                m.d.comb += self.o_ma1.eq(0x275)
            with m.Case('0100---111111001--'):
                m.d.comb += self.o_ma1.eq(0x3e4)
            with m.Case('0100111010111011--'):
                m.d.comb += self.o_ma1.eq(0x1f3)
            with m.Case('0100111010110-----'):
                m.d.comb += self.o_ma1.eq(0x1f3)
            with m.Case('0100111010111010--'):
                m.d.comb += self.o_ma1.eq(0x2b0)
            with m.Case('0100111010101-----'):
                m.d.comb += self.o_ma1.eq(0x2b0)
            with m.Case('0100111010010-----'):
                m.d.comb += self.o_ma1.eq(0x273)
            with m.Case('0100111010111000--'):
                m.d.comb += self.o_ma1.eq(0x293)
            with m.Case('0100111010111001--'):
                m.d.comb += self.o_ma1.eq(0x1f2)
            with m.Case('0100111011111011--'):
                m.d.comb += self.o_ma1.eq(0x1f7)
            with m.Case('0100111011110-----'):
                m.d.comb += self.o_ma1.eq(0x1f7)
            with m.Case('0100111011111010--'):
                m.d.comb += self.o_ma1.eq(0x2b4)
            with m.Case('0100111011101-----'):
                m.d.comb += self.o_ma1.eq(0x2b4)
            with m.Case('0100111011010-----'):
                m.d.comb += self.o_ma1.eq(0x255)
            with m.Case('0100111011111000--'):
                m.d.comb += self.o_ma1.eq(0x297)
            with m.Case('0100111011111001--'):
                m.d.comb += self.o_ma1.eq(0x1f6)
            with m.Case('----------1111001-'):
                m.d.comb += self.o_ma1.eq(0x0ea)
            with m.Case('----------111100-1'):
                m.d.comb += self.o_ma1.eq(0x0a7)
            with m.Case('0100100011000-----'):
                m.d.comb += self.o_ma1.eq(0x232)
            with m.Case('1100---110001-----'):
                m.d.comb += self.o_ma1.eq(0x3e3)
            with m.Case('1100---10100------'):
                m.d.comb += self.o_ma1.eq(0x3e3)
            with m.Case('1000---011000-----'):
                m.d.comb += self.o_ma1.eq(0x0a6)
            with m.Case('1000---111000-----'):
                m.d.comb += self.o_ma1.eq(0x0ae)
            with m.Case('0101----11001-----'):
                m.d.comb += self.o_ma1.eq(0x06c)
            with m.Case('1011---00-00------'):
                m.d.comb += self.o_ma1.eq(0x1d1)
            with m.Case('1011---01100------'):
                m.d.comb += self.o_ma1.eq(0x1d9)
            with m.Case('1011---11100------'):
                m.d.comb += self.o_ma1.eq(0x1d5)
            with m.Case('1011---01000------'):
                m.d.comb += self.o_ma1.eq(0x1d5)
            with m.Case('1011---110001-----'):
                m.d.comb += self.o_ma1.eq(0x06f)
            with m.Case('1011---10-001-----'):
                m.d.comb += self.o_ma1.eq(0x06b)
            with m.Case('0100---110000-----'):
                m.d.comb += self.o_ma1.eq(0x152)
            with m.Case('0000---100000-----'):
                m.d.comb += self.o_ma1.eq(0x3e7)
            with m.Case('0100101010000-----'):
                m.d.comb += self.o_ma1.eq(0x125)
            with m.Case('0000---1-1000-----'):
                m.d.comb += self.o_ma1.eq(0x3ef)
            with m.Case('0000---110000-----'):
                m.d.comb += self.o_ma1.eq(0x3eb)
            with m.Case('0100111001110110--'):
                m.d.comb += self.o_ma1.eq(0x06d)
            with m.Case('010011100100------'):
                m.d.comb += self.o_ma1.eq(0x1d0)
            with m.Case('0100101011000-----'):
                m.d.comb += self.o_ma1.eq(0x345)
            with m.Case('0100111001110001--'):
                m.d.comb += self.o_ma1.eq(0x363)
            with m.Case('1-01---10-001-----'):
                m.d.comb += self.o_ma1.eq(0x10f)
            with m.Case('1-01---110001-----'):
                m.d.comb += self.o_ma1.eq(0x10b)
            with m.Case('1-00---100001-----'):
                m.d.comb += self.o_ma1.eq(0x107)
            with m.Case('----------1110111-'):
                m.d.comb += self.o_ma1.eq(0x1e3)
            with m.Case('----------110---1-'):
                m.d.comb += self.o_ma1.eq(0x1e3)
            with m.Case('----------111011-1'):
                m.d.comb += self.o_ma1.eq(0x1e7)
            with m.Case('----------110----1'):
                m.d.comb += self.o_ma1.eq(0x1e7)
            with m.Case('----------1110101-'):
                m.d.comb += self.o_ma1.eq(0x1c2)
            with m.Case('----------101---1-'):
                m.d.comb += self.o_ma1.eq(0x1c2)
            with m.Case('----------111010-1'):
                m.d.comb += self.o_ma1.eq(0x1c6)
            with m.Case('----------101----1'):
                m.d.comb += self.o_ma1.eq(0x1c6)
            with m.Case('----------010---1-'):
                m.d.comb += self.o_ma1.eq(0x006)
            with m.Case('----------010----1'):
                m.d.comb += self.o_ma1.eq(0x00b)
            with m.Case('----------1110001-'):
                m.d.comb += self.o_ma1.eq(0x00a)
            with m.Case('----------111000-1'):
                m.d.comb += self.o_ma1.eq(0x00e)
            with m.Case('----------1110011-'):
                m.d.comb += self.o_ma1.eq(0x1e2)
            with m.Case('----------111001-1'):
                m.d.comb += self.o_ma1.eq(0x1e6)

        ma23ctx = Signal(2)
        m.d.comb += ma23ctx[0].eq(self.i_ird.matches("0000------------"))
        m.d.comb += ma23ctx[1].eq(self.i_ird.matches("-------010------"))

        m.d.comb += self.o_ma2.eq(0x3ff)
        m.d.comb += self.o_ma3.eq(0x3ff)
        with m.Switch(Cat(self.i_ird, ma23ctx)):
            with m.Case("--1100----11------"):
                m.d.comb += [ self.o_ma3.eq(0x15a), self.o_ma2.eq(0x15b) ]
            with m.Case("--1011---011------"):
                m.d.comb += [ self.o_ma3.eq(0x1cf), self.o_ma2.eq(0x1d9) ]
            with m.Case("--1011---00-------"):
                m.d.comb += [ self.o_ma3.eq(0x1d3), self.o_ma2.eq(0x1d1) ]
            with m.Case("--1011---111------"):
                m.d.comb += [ self.o_ma3.eq(0x1d7), self.o_ma2.eq(0x1d5) ]
            with m.Case("--00-1---100------"):
                m.d.comb += [ self.o_ma3.eq(0x38b), self.o_ma2.eq(0x2f8) ]
            with m.Case("--1000---111------"):
                m.d.comb += [ self.o_ma3.eq(0x0ac), self.o_ma2.eq(0x0ae) ]
            with m.Case("--1000---011------"):
                m.d.comb += [ self.o_ma3.eq(0x0a4), self.o_ma2.eq(0x0a6) ]
            with m.Case("--1-01---111------"):
                m.d.comb += [ self.o_ma3.eq(0x1cb), self.o_ma2.eq(0x1c5) ]
            with m.Case("--00-1---011------"):
                m.d.comb += [ self.o_ma3.eq(0x3af), self.o_ma2.eq(0x2fe) ]
            with m.Case("--1-01---011------"):
                m.d.comb += [ self.o_ma3.eq(0x1c7), self.o_ma2.eq(0x1c9) ]
            with m.Case("--1-0----00-------"):
                m.d.comb += [ self.o_ma3.eq(0x1c3), self.o_ma2.eq(0x1c1) ]
            with m.Case("--0100---110------"):
                m.d.comb += [ self.o_ma3.eq(0x151), self.o_ma2.eq(0x152) ]
            with m.Case("--010001-011------"):
                m.d.comb += [ self.o_ma3.eq(0x159), self.o_ma2.eq(0x301) ]
            with m.Case("--00-1001111------"):
                m.d.comb += [ self.o_ma3.eq(0x32b), self.o_ma2.eq(0x1ea) ]
            with m.Case("--0010001111------"):
                m.d.comb += [ self.o_ma3.eq(0x30f), self.o_ma2.eq(0x1ee) ]
            with m.Case("--0010000111------"):
                m.d.comb += [ self.o_ma3.eq(0x38c), self.o_ma2.eq(0x2dd) ]
            with m.Case("--0010---110------"):
                m.d.comb += [ self.o_ma3.eq(0x29c), self.o_ma2.eq(0x1ef) ]
            with m.Case("--0010---101------"):
                m.d.comb += [ self.o_ma3.eq(0x38e), self.o_ma2.eq(0x2de) ]
            with m.Case("--0010---100------"):
                m.d.comb += [ self.o_ma3.eq(0x38f), self.o_ma2.eq(0x2fc) ]
            with m.Case("--0010---011------"):
                m.d.comb += [ self.o_ma3.eq(0x3ad), self.o_ma2.eq(0x2fd) ]
            with m.Case("--00-1---000------"):
                m.d.comb += [ self.o_ma3.eq(0x29b), self.o_ma2.eq(0x121) ]
            with m.Case("--0010---00-------"):
                m.d.comb += [ self.o_ma3.eq(0x29f), self.o_ma2.eq(0x129) ]
            with m.Case("--0011---001------"):
                m.d.comb += [ self.o_ma3.eq(0x158), self.o_ma2.eq(0x279) ]
            with m.Case("--00-1000111------"):
                m.d.comb += [ self.o_ma3.eq(0x388), self.o_ma2.eq(0x2d9) ]
            with m.Case("--00-1---110------"):
                m.d.comb += [ self.o_ma3.eq(0x298), self.o_ma2.eq(0x1eb) ]
            with m.Case("--00-1---101------"):
                m.d.comb += [ self.o_ma3.eq(0x38a), self.o_ma2.eq(0x2da) ]
            with m.Case("1-1011------------"):
                m.d.comb += [ self.o_ma3.eq(0x1d7), self.o_ma2.eq(0x1d5) ]
            with m.Case("1-1-0-------------"):
                m.d.comb += [ self.o_ma3.eq(0x1cb), self.o_ma2.eq(0x1c5) ]
            with m.Case("1-00-1------------"):
                m.d.comb += [ self.o_ma3.eq(0x3ab), self.o_ma2.eq(0x2fa) ]
            with m.Case("1-0010------------"):
                m.d.comb += [ self.o_ma3.eq(0x3a9), self.o_ma2.eq(0x2f9) ]
            with m.Case("-1-------100------"):
                m.d.comb += [ self.o_ma3.eq(0x215), self.o_ma2.eq(0x0ab) ]
            with m.Default():
                with m.Switch(Cat(self.i_ird, ma23ctx)):
                    with m.Case("--0101----11------"):
                        m.d.comb += self.o_ma3.eq(0x380)
                    with m.Case("--0101----10------"):
                        m.d.comb += self.o_ma3.eq(0x2f7)
                    with m.Case("--0101----0-------"):
                        m.d.comb += self.o_ma3.eq(0x2f3)
                    with m.Case("--0100101011------"):
                        m.d.comb += self.o_ma3.eq(0x343)
                    with m.Case("--1------110------"):
                        m.d.comb += self.o_ma3.eq(0x29d)
                    with m.Case("--010010100-------"):
                        m.d.comb += self.o_ma3.eq(0x3c3)
                    with m.Case("--0100100000------"):
                        m.d.comb += self.o_ma3.eq(0x15c)
                    with m.Case("--0100000011------"):
                        m.d.comb += self.o_ma3.eq(0x3a1)
                    with m.Case("--01000--00-------"):
                        m.d.comb += self.o_ma3.eq(0x2b8)
                    with m.Case("1-01000-----------"):
                        m.d.comb += self.o_ma3.eq(0x2bc)
                    with m.Case("1-0100101---------"):
                        m.d.comb += self.o_ma3.eq(0x3cb)
                    with m.Case("-1-------110------"):
                        m.d.comb += self.o_ma3.eq(0x069)
                    with m.Case("11----110---------"):
                        m.d.comb += self.o_ma3.eq(0x08f)
                    with m.Case("11----100---------"):
                        m.d.comb += self.o_ma3.eq(0x069)
                    with m.Case("11----------------"):
                        m.d.comb += self.o_ma3.eq(0x29d)
                    with m.Case("--11100---11------"):
                        m.d.comb += self.o_ma3.eq(0x3c7)
                    with m.Case("--1------10-------"):
                        m.d.comb += self.o_ma3.eq(0x299)
                    with m.Case("-1----11000-------"):
                        m.d.comb += self.o_ma3.eq(0x087)
                    with m.Case("-1-------1-1------"):
                        m.d.comb += self.o_ma3.eq(0x081)
                    with m.Case("-1----1000-1------"):
                        m.d.comb += self.o_ma3.eq(0x081)
                    with m.Case("-1----100000------"):
                        m.d.comb += self.o_ma3.eq(0x215)
                    with m.Case("-1-------00-------"):
                        m.d.comb += self.o_ma3.eq(0x299)

                with m.Switch(Cat(self.i_ird, ma23ctx)):
                    with m.Case("11----110---000---"):
                        m.d.comb += self.o_ma2.eq(0x104)
                    with m.Case("11----100---000---"):
                        m.d.comb += self.o_ma2.eq(0x3eb)
                    with m.Case("11----------000---"):
                        m.d.comb += self.o_ma2.eq(0x10c)
                    with m.Case("-1-------00-111100"):
                        m.d.comb += self.o_ma2.eq(0x1cc)
                    with m.Case("-1----1000-1000---"):
                        m.d.comb += self.o_ma2.eq(0x3ef)
                    with m.Case("-1----100000000---"):
                        m.d.comb += self.o_ma2.eq(0x3e7)
                    with m.Case("-1----11000-000---"):
                        m.d.comb += self.o_ma2.eq(0x108)
                    with m.Case("-1-------00-000---"):
                        m.d.comb += self.o_ma2.eq(0x100)
                    with m.Case("11----0-----011---"):
                        m.d.comb += self.o_ma2.eq(0x00f)
                    with m.Case("11-----1----011---"):
                        m.d.comb += self.o_ma2.eq(0x00f)
                    with m.Case("11------1---011---"):
                        m.d.comb += self.o_ma2.eq(0x00f)
                    with m.Case("-1-------0--011---"):
                        m.d.comb += self.o_ma2.eq(0x21c)
                    with m.Case("11----0-----100---"):
                        m.d.comb += self.o_ma2.eq(0x179)
                    with m.Case("11-----1----100---"):
                        m.d.comb += self.o_ma2.eq(0x179)
                    with m.Case("11------1---100---"):
                        m.d.comb += self.o_ma2.eq(0x179)
                    with m.Case("-1-------0--100---"):
                        m.d.comb += self.o_ma2.eq(0x103)
                    with m.Case("11----0-----101---"):
                        m.d.comb += self.o_ma2.eq(0x1c6)
                    with m.Case("11-----1----101---"):
                        m.d.comb += self.o_ma2.eq(0x1c6)
                    with m.Case("11------1---101---"):
                        m.d.comb += self.o_ma2.eq(0x1c6)
                    with m.Case("-1----100000111010"):
                        m.d.comb += self.o_ma2.eq(0x1c2)
                    with m.Case("-1-------0--101---"):
                        m.d.comb += self.o_ma2.eq(0x1c2)
                    with m.Case("11----0-----110---"):
                        m.d.comb += self.o_ma2.eq(0x1e7)
                    with m.Case("11-----1----110---"):
                        m.d.comb += self.o_ma2.eq(0x1e7)
                    with m.Case("11------1---110---"):
                        m.d.comb += self.o_ma2.eq(0x1e7)
                    with m.Case("-1----100000111011"):
                        m.d.comb += self.o_ma2.eq(0x1e3)
                    with m.Case("-1-------0--110---"):
                        m.d.comb += self.o_ma2.eq(0x1e3)
                    with m.Case("11----0-----111000"):
                        m.d.comb += self.o_ma2.eq(0x00e)
                    with m.Case("11-----1----111000"):
                        m.d.comb += self.o_ma2.eq(0x00e)
                    with m.Case("11------1---111000"):
                        m.d.comb += self.o_ma2.eq(0x00e)
                    with m.Case("-1-------0--111000"):
                        m.d.comb += self.o_ma2.eq(0x00a)
                    with m.Case("11----0-----111001"):
                        m.d.comb += self.o_ma2.eq(0x1e6)
                    with m.Case("11-----1----111001"):
                        m.d.comb += self.o_ma2.eq(0x1e6)
                    with m.Case("11------1---111001"):
                        m.d.comb += self.o_ma2.eq(0x1e6)
                    with m.Case("-1-------0--111001"):
                        m.d.comb += self.o_ma2.eq(0x1e2)
                    with m.Case("11----0-----010---"):
                        m.d.comb += self.o_ma2.eq(0x00b)
                    with m.Case("11-----1----010---"):
                        m.d.comb += self.o_ma2.eq(0x00b)
                    with m.Case("11------1---010---"):
                        m.d.comb += self.o_ma2.eq(0x00b)
                    with m.Case("-1-------0--010---"):
                        m.d.comb += self.o_ma2.eq(0x006)

        return m
