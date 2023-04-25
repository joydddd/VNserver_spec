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
## slice size of 1b, native icelake arch
```
./looppoint/run-looppoint.py -c $(LOOPPOINT_CFG) -n 8 --force **<--reuse-profile> --no-validate
```
|   Testbench           |   pinballs    |   BBV         |   Simpoint    |   sniper      | comments |
|-----------------------|---------------|---------------|---------------|---------------|----------|
|   tags                |   [log_whole] |   [gen_BBV]   |  [Simpoint]   |   [SNIPER]    |
|   600.perlbench_s.0   |   finish      |   finish      |   finish      |  `20230425160758` running r1 using `cache-only` | Apr 25 16:07
|   600.perlbench_s.1   |   finish      |   finish      |   finish      |  `20230420163100` running r6 using `detailed`, trace generated   | Apr 24 19:21
|   600.perlbench_s.2   |   finish      |   finish      |   finish      |  `20230421212559` running r4 using `cache-only`, trace generated   | Apr 25 07:21
|   602.gcc_s.0         |   finish      |   ==seg fault==   |               |               |
|   602.gcc_s.1         |   finish      |   ==seg fault==   |               |               |
|   602.gcc_s.2         |   finish      |   ==seg fault==   |               |               |
|   605.mcf_s           |   finish      |   finish      |   finish      |   `20230418220545` running r3 using `detailed`, trace generated | Apr 21 14:56
|   620.omnetpp_s       |   finish      |   finish      |   finish      |   `20230418220039` running r5 using `detailed`, trace generated | Apr 25 13:30
|   625.x264_s.0        |   finish      |   finish      |   finish      |   `20230420162754` running r7 using `detailed`, trace generated | Apr 25 12:03
|   625.x264_s.1        |   finish      |   finish      |   finish      |   `20230421211306` running r3 using `cache-only`, ==no trace generated== | Apr 24 08:44
|   625.x264_s.2        |   finish      |   finish      |   finish      |   `20230425155842` running r1 using `cache-only` | Apr 25 15:58
|   631.deepsjeng_s     |   finish      |   finish      |       finish  |   `20230421205749` running r1 using `cache-only` | Apr 21 20:57 
|   648.exchange2_s     |   finish      |   finish      |       finish  |   `20230421212103` running r3 using `cache-only`, ==no trace generated==  | Apr 25 06:19
|   657.xz_s.0          |   ==ERROR==   |               |               |                                       |*native run successful* 
|   657.xz_s.1          |   ==ERROR==     |               |               |                                       |*native run successful* 


### 625.x264_s.1
```
yuv [info]: 1280x720p 0:0 @ 25/1 fps (cfr)
x264 [info]: using cpu capabilities: none!
x264 [error]: 2nd pass has more frames than 1st pass (1000 vs 282)
x264 [error]: x264_encoder_open failed
```