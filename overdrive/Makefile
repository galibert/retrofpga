YOSYS = ../../yosys

BASE = overdrive.py
COMPONENTS = ../k053252/k053252.py

overdrive: main.cc overdrive.cc
	clang++ -O3 -I${YOSYS}/backends/cxxrtl main.cc -o overdrive

overdrive.cc: yosys.cmd
	yosys -qs $< > $@

yosys.cmd: ${BASE} ${COMPONENTS}
	python ${BASE} > yosys.cmd

clean:
	rm -f yosys.cmd overdrive.cc overdrive
