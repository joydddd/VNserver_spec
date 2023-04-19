#!/usr/bin/python
SPEC_ROOT = "/home/joydong/Desktop/snipersim/spec"

import sys
import os
TEST_BENCH = sys.argv[1]

f_run_sh = open(os.path.join(SPEC_ROOT, "spec_bin", TEST_BENCH + "_run", "run.sh"), 'r')
run_sh_lines = f_run_sh.readlines()
count = 0

for line in run_sh_lines:
    if line.startswith("./app"):
        default_run_dir = os.path.join(SPEC_ROOT, "spec_bin", TEST_BENCH + "_run")
        if count == 0:
            run_dir = default_run_dir
        else:
            run_dir = os.path.join(SPEC_ROOT, "spec_bin", TEST_BENCH + "_run.%(count)s" % locals())
        f_cfg_path = os.path.join(run_dir, TEST_BENCH + "." + str(count) + ".cfg")
        print(f_cfg_path)
        
        if not os.path.exists(run_dir): # copy running dir from default dir if doesn't exist
            os.system('cp -r %(default_run_dir)s/. %(run_dir)s' % locals())
        
        if not os.path.isfile(f_cfg_path): # gen config file if doesn not exist
            f_cfg = open(f_cfg_path, 'w+')
            f_cfg.write(r"""[Parameters]
program_name: app
input_name: %(count)s
command: %(line)s""" % locals())
            
        count += 1