YOSYS = ../../yosys

BASE = gen.py
COMPONENTS = overdrive.py ../k053252/k053252.py ../k051316/k051316.py

overdrive: main.cc overdrive.cc
	clang++ -O3 -I${YOSYS}/backends/cxxrtl main.cc -o overdrive -lz

overdrive.cc: yosys.cmd
	yosys -qs $< > $@

yosys.cmd: ${BASE} ${COMPONENTS}
	python ${BASE} > yosys.cmd

clean:
	rm -f yosys.cmd overdrive.cc overdrive
