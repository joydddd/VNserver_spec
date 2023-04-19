# Experiment Setups
### generate regional pinballs of SPEC CPU2017 benchmark 

### Simpoint

### Simulate with SniperSim
#### Run SPEC natively with out `runcpu`
https://www.spec.org/cpu2006/Docs/runspec-avoidance.html
`make gen_sim`

http://snipersim.org/documents/2013-02-23%20PinPoints%20Sniper%20HPCA%20Tutorial.pdf
PinPoints + Sniper Tutorial

https://github.com/intel/pinplay-tools
pinplay-tools created by Intel


https://github.com/nus-comparch/looppoint/tree/acdb54f1897373f945e5a608090dc7d3dcec77ea
Looppoint: HPCA 2022 Multi-threaded Application Simulation! !!Thank God they have all the scripts I need!!!! 

# Current Running Simulations
slice size of 1b 
```
./looppoint/run-looppoint.py -c $(LOOPPOINT_CFG) -n 8 --force **<--reuse-profile> --no-validate
```
|   Testbench           |   pinballs    |   BBV         |   Simpoint    |   sniper      |
|-----------------------|---------------|---------------|---------------|---------------|
|   /                   |   [log_whole] |   [gen_BBV]   |  [Simpoint]   |   [SNIPER]    |
|   600.perlbench_s.0   |   finish      |   finish      |   finish      |   restarted using `--reuse-profile`  |
|   600.perlbench_s.1   |   running     |
|   600.perlbench_s.2   |   running     |
|   602.gcc_s.0         |   finish      |   seg fault   |               |               |
|   602.gcc_s.1         |   
|   602.gcc_s.2         |
|   605.mcf_s           |   finish      |   finish      |   finish      |   restarted using `--reuse-profile`  |
|   620.omnetpp_s       |   finish      |   finish      |   finish      |   restarted using `--reuse-profile`   |
|   625.x264_s.0        |   running     |
|   625.x264_s.1        |   running     |
|   625.x264_s.2        |   running     |
|   631.deepsjeng_s     |   finish      |   finish      |     finish    |   restarted using `--reuse-profile`   |
|   648.exchange2_s     |   finish      |   running     |               |               |
|   657.xz_s.0          |   running native run
|   657.xz_s.1          |
