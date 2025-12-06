export PYTHONPATH := $(PWD)/../../:$(PYTHONPATH)
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/test.sv
TOPLEVEL = test
MODULE = testcase
EXTRA_ARGS += --trace --trace-fst --trace-structs
include $(shell cocotb-config --makefiles)/Makefile.sim