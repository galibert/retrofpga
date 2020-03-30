YOSYS = ../../yosys

BASE = gen.py
COMPONENTS = via6522.py

via6522: main.cc via6522.cc
	clang++ -O3 -I${YOSYS}/backends/cxxrtl main.cc -o via6522 -lz

via6522.cc: yosys.cmd
	yosys -qs $< > $@

yosys.cmd: ${BASE} ${COMPONENTS}
	python ${BASE} > yosys.cmd

clean:
	rm -f yosys.cmd via6522.cc via6522
