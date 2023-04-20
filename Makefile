# TEST_BENCH := intspeed
TEST_BENCH := 600.perlbench_s 602.gcc_s 605.mcf_s 620.omnetpp_s 625.x264_s 631.deepsjeng_s 648.exchange2_s 657.xz_s
LOOPPOINT_CFG := /home/joydong/Desktop/snipersim/spec/spec_bin/602.gcc_s_run/602.gcc_s.0.cfg

all : spec_build gen_spec_run_cmd gen_looppoint_cfg

spec_fake_run: $(addprefix spec_fake_run_, $(TEST_BENCH))
spec_fake_run_%: 
	@. ./build_test.sh && fake_run_spec $(@:spec_fake_run_%=%)

spec_build: $(addprefix spec_bin/, $(TEST_BENCH))
spec_bin/%:
	@. ./build_test.sh && build_spec $(notdir $@)

gen_spec_run: $(addprefix gen_spec_run_, $(TEST_BENCH))
gen_spec_run_%: spec_bin/%
	@. ./build_test.sh && gen_spec_run_cmd $(@:gen_spec_run_%=%)

gen_looppoint_cfg: $(addprefix gen_looppoint_cfg_, $(TEST_BENCH))
gen_looppoint_cfg_%:
	@./gen_looppoint_cfg.py $(@:gen_looppoint_cfg_%=%)

spec_run_%: 
	spec_bin/$(@:spec_run_%=%)_run/run.sh

looppoint_run:
	./looppoint/run-looppoint.py -c $(LOOPPOINT_CFG) -n 8 --force --reuse-profile --no-validate

looppoint_run_new:
	./looppoint/run-looppoint.py -c $(LOOPPOINT_CFG) -n 8 --force --no-validate