YOSYS = /people/galibert

BASE = gen.py
COMPONENTS = m68000.py eclock.py idecode.py microcode.py
OPT=-O3

m68000: main.cc m68000.cc
	clang++ -g3 ${OPT} -I${YOSYS}/share/yosys/include main.cc -o m68000

m68000.cc: yosys.cmd
	yosys -qs $< > $@

yosys.cmd: ${BASE} ${COMPONENTS}
	python ${BASE} > yosys.cmd

clean:
	rm -f yosys.cmd m68000.cc m68000
