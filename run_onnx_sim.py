#!/usr/bin/python3

import os
import datetime

SPEC_ROOT = os.getcwd()
onnx_set = ['3dunet', 'resnet']
genome_set = ['fmi', 'fmi-l', 'bsw', 'bsw-l', 'dbg', 'chain', 'kmer-cnt', 'pileup', 'bsw-s']
graph_set = ['pr', 'pr-kron', 'pr-kron-s', 'pr_spmv', 'sssp', 'bfs', 'bc', 'cc', 'cc_sv', 'tc']
sim_test = ['bsw-s', 'pr-kron-s'] # small test cases for testing simulators
test_set = ['bsw-s']

config = {}
config['simulator'] = 'vnsniper'
# config['simulator'] = 'sniper'


# config['arch'] = 'zen4_s'
config['arch'] = 'zen4_cxl'
config['ncores'] = 32


# config['arch'] = 'coaxial_s'
# config['ncores'] = 12

# config['arch'] = 'icelake_s'
# config['arch'] = 'icelake_cxl'
# config['arch'] = 'icelake_vn'
# config['ncores'] = 10

G1 = 1000000000 # 1bilion
M100 = 100000000 # 100 million
M1 = 1000000 # 1 million


benches = {}
benches['resnet'] = {
    'cmd'   : '../../build/Linux/Release/onnx -r 1 -c 1 -x %(ncores)s ex/resnet50-v1-12.onnx -D' % config,
    # pin_hook_init Global icount: 180325165538
    # pin_hook_fini Global icount: 359314218609// 178,989,053,071
    'regions' : [ {'name': 'r1', 'ff_icount' : 100989053071, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                  {'name': 'r2', 'ff_icount' : 50989053071, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000}]
}

benches['3dunet'] = {
    'cmd'   : '../../build/Linux/Release/onnx -r 1 -c 1 -x %(ncores)s ex/model.onnx -D' % config,
    # pin_hook_init Global icount: 430082223621
    # pin_hook_fini Global icount: 860865205136 // 430,782,981,515
    'regions' : [
                 {'name': 'r1', 'ff_icount' : 230782981515, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                 {'name': 'r2', 'ff_icount' : 130782981515, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                 {'name': 'r3', 'ff_icount' : 330782981515, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                 {'name': 'r4', 'ff_icount' : 60782981515, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }
                 ]
}

benches['fmi'] = {
    'cmd' : './fmi ../../input-datasets/fmi/broad ../../input-datasets/fmi/small/SRR7733443_1m_1.fastq 512 19 %(ncores)s' % config,
    # pin_hook_init global icount: 11076996653
    # pin_hook_fini global icount: 173932537459 // 162,855,540,806
    'regions': [{'name': 'r1', 'ff_icount' : 82855540806, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }, 
                {'name': 'r2', 'ff_icount' : 42855540806, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['fmi-l'] = {
    'cmd' : './fmi ../../input-datasets/fmi/broad ../../input-datasets/fmi/large/SRR7733443_10m_1.fastq 512 19 %(ncores)s' % config,
    # pin_hook_init global icount: 110,252,278,764
    # pin_hook_fini global icount: 1,823,920,288,894 // 1,713,668,010,130
    'regions': [{'name': 'r1-t32', 'ff_icount' : 610202535318, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 1100202535318, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }]
}

benches['bsw'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/large/bandedSWA_SRR7733443_500k_input.txt  -t %(ncores)s -b 512' % config,
    # pin_hook_init global icount: 11174244380
    # pin_hook_fini global icount: 170256191236 // 159,081,946,856
    'regions': [{'name': 'r1', 'ff_icount' : 89081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 49081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['bsw-l'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/large/bandedSWA_SRR7733443_1m_input.txt  -t %(ncores)s -b 512' % config,
    # pin_hook_init global icount: 23,484,072,677
    # pin_hook_fini global icount: 721,547,029,143 // 698,062,956,466
    'regions': [{'name': 'r1-t32', 'ff_icount' : 223568924357, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 423568924357, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }]
}


benches['bsw-s'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/small/bandedSWA_SRR7733443_100k_input.txt  -t %(ncores)s -b 512' % config,
    'regions': [{'name': 'r1-t32', 'ff_icount' : 3238814760, 'warmup_icount' : M1*32, 'sim_icount' : M1*32, 'ncores': 32 }]
}

benches['dbg'] = {
    'cmd' : './dbg ../../input-datasets/dbg/large/ERR194147-mem2-chr22.bam chr22:0-50818468 ../../input-datasets/dbg/large/Homo_sapiens_assembly38.fasta %(ncores)s' % config,
    # pin_hook_init global icount: 135,442,369,317
    # pin_hook_fini global icount: 2,252,177,293,572 // 2,116,734,924,255
    'regions': [{'name': 'r1', 'ff_icount' : 1116734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 516734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r3', 'ff_icount' : 1516734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : 835447539618, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 1635447539618, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }]
}

benches['chain'] = {
    'cmd' : './chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t %(ncores)s' % config,
    # pin_hook_init global icount: 897,270,215,617
    # pin_hook_fini global icount: 1,337,813,610,738 // 440,543,395,121
    'regions': [
                {'name': 'r1', 'ff_icount' : 230543395121, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 130543395121, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : 140593939208, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 340593939208, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ]
}

benches['kmer-cnt'] = {
    'cmd' : './kmer-cnt --reads ../../input-datasets/kmer-cnt/large/Loman_E.coli_MAP006-1_2D_50x.fasta --config ../../tools/Flye/flye/config/bin_cfg/asm_raw_reads.cfg --threads %(ncores)s' % config,
    'regions': []
}

benches['pileup'] = {
    'cmd' : './pileup ../../input-datasets/pileup/large/HG002_prom_R941_guppy360_2_GRCh38_ch20.bam chr20:1-64444167 %(ncores)s ' % config,
    # pin_hook_init global icount:14,246,308
    # pin_hook_fini global icount: 1,050,781,289,380 // 1,050,767,043,072
    'regions': [{'name': 'r1', 'ff_icount' : 250767043072, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 650767043072, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : G1*300, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': G1*600, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }]
}

benches['pr'] = {
    'cmd' : '../../pr -f ../../webbase-2001/webbase-2001.mtx -n 1',
    # pin_hook_init global icount: 4,584,727,445,620
    # pin_hook_fini global icount: 4,730,536,799,846 // 145,809,354,226
    'regions': [{'name': 'r1', 'ff_icount' : 105809354226, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 45809354226, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}


## -g26
# benches['pr-kron'] = {
#     'cmd' : '../../pr -f ../../benchmark/graphs/kron.sg -n 1',
#     # t = 10
#     # pin_hook_init global icount: 496,327,755
#     # pin_hook_fini global icount: 62,255,172,042 // 61,758,844,287
#     # t = 12
#     # pin_hook_init global icount: 502,030,597
#     # pin_hook_fini global icount: 62,299,143,638 // 61,797,113,041
#     # t = 32
#     # pin_hook_init global icount: 502,851,793
#     # pin_hook_init global icount: 62,564,119,587 // 62,061,267,794
#     'regions': [{'name': 'r1', 'ff_icount' : 11758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
#                 {'name': 'r2', 'ff_icount' : 41758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
#                 {'name': 'r1-t12', 'ff_icount' : 11758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000, 'ncores': 12 },
#                 {'name': 'r2-t12', 'ff_icount': 41758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000, 'ncores': 12 },
#                 {'name': 'r1-t32', 'ff_icount' : 11758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000, 'ncores': 32 },
#                 {'name': 'r2-t32', 'ff_icount': 41758844287, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000, 'ncores': 32 }
#                 ]
# }

# -g27
benches['pr-kron'] = {
    'cmd' : '../../pr -f ../../benchmark/graphs/kron-g27.sg -n 1',
    # t = 32
    # pin_hook_init global icount: 1,085,882,166
    # pin_hook_fini global icount: 125,263,751,069 // 124,177,868,903
    'regions': [
                {'name': 'r1-t32', 'ff_icount' : G1*30, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': G1*80, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ]
}

benches['pr-kron-s'] = {
    'cmd' : '../../pr -f ../../benchmark/graphs/kron-g22.sg -n 1',
    'regions': [{'name': 'r1-t32', 'ff_icount' : 2068478955, 'warmup_icount' : M1*32, 'sim_icount' : M1*32, 'ncores': 32 }]
}

benches['pr_spmv'] = {
    'cmd' : '../../pr_spmv -f ../../webbase-2001/webbase-2001.mtx -n 1',
    # pin_hook_init global icount: 4585059346044
    # pin_hook_fini global icount: 4752972186227 // 167,912,840,183
    'regions': [{'name': 'r1', 'ff_icount' : 107912840183, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 57912840183, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['sssp'] = {
    'cmd' : '../../sssp -f ../../GAP-road/GAP-road.mtx -n 1 -r 64',
    'regions': []
}

benches['bfs'] = {
    'cmd' : '../../bfs -f ../../GAP-urand/GAP-urand.mtx -n 1',
}

benches['bc'] = {
    'cmd' : '../../bc -f ../../GAP-road/GAP-road.mtx -n 1',
}

benches['cc'] = {
    'cmd' : '../../cc -f ../../GAP-twitter/GAP-twitter.mtx -n 1',
}

benches['cc_sv'] = {
    'cmd' : '../../cc_sv -f ../../webbase-2001/webbase-2001.mtx -n 1',
    # pin_hook_init global icount: 4584898946423
    # pin_hook_fini global icount: 4684589336834 // 99,690,390,411
    'regions': [{'name': 'r1', 'ff_icount' : 69690390411, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 39690390411, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['tc'] = {
    'cmd' : '../../tc -f ../../mycielskian20/mycielskian20.mtx -n 1',
}


###################### Sniper Commands ######################
sniper_command = '$SNIPER_ROOT/run-sniper       -n %(ncores)s     -v -sprogresstrace:10000000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming -ssimuserwarmup --roi-script --trace-args="-pinplay:control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global"  --trace-args="-pinplay:controller_log 1"  --trace-args="-pinplay:controller_olog %(sim_results_dir)s/pinplay_controller.log" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/oneipc/include_memory_latency=false -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'

sniper_command_gdb = '$SNIPER_ROOT/run-sniper       -n %(ncores)s  --gdb-wait   -v -sprogresstrace:10000000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming -ssimuserwarmup --roi-script --trace-args="-pinplay:control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global"  --trace-args="-pinplay:controller_log 1"  --trace-args="-pinplay:controller_olog %(sim_results_dir)s/pinplay_controller.log" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/oneipc/include_memory_latency=false -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'

region_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count %(ncores)s -control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'

roi_icount_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count %(ncores)s -control start:address:pin_hook_init,stop:address:pin_hook_fini -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'


native_commamd = '/usr/bin/time -v %(exe_command)s 2>&1 | tee %(output_path)s/sniper.out'

os.environ["SPEC_ROOT"] = SPEC_ROOT
os.environ["SDE_BUILD_KIT"] = os.path.join(SPEC_ROOT, 'sde')
os.environ["PINBALL2ELF"] =  os.path.join(SPEC_ROOT, 'pinball2elf')
os.environ["SNIPER_ROOT"] = os.path.join(SPEC_ROOT, config['simulator'])
os.environ["OMP_NUM_THREADS"] = str(config['ncores'])

onnx_model_path = os.path.join(SPEC_ROOT, 'onnxruntime/models')
genom_bench_path = os.path.join(SPEC_ROOT, 'genomicsbench/benchmarks')
gapbs_bench_path = os.path.join(SPEC_ROOT, 'gapbs/run')

def run_native(bench):
    print("******************* Running native " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path
    bench_path = os.path.join(path, bench)
    output_path = os.path.join(bench_path, 'native-run')
    os.chdir(bench_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    exe_command = benches[bench]['cmd']
    print(native_commamd % {**locals(), **config})
    os.system(native_commamd % {**locals(), **config})
        
def run_sniper(bench):
    print("******************* Running sniper " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    sim_results_dir_root = 'sim-{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
    print("Simulation name: " + sim_results_dir_root)
    sim_results_dir_root = os.path.join(bench_path, sim_results_dir_root)
    os.makedirs(sim_results_dir_root)
    exe_command = benches[bench]['cmd']
    for r in benches[bench]['regions']:
        try: 
            if config['ncores'] != 10 and r['ncores'] != config['ncores']:
                continue
        except(KeyError):
            continue
        
        sim_results_dir = os.path.join(sim_results_dir_root, r['name'])
        os.makedirs(sim_results_dir)
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        
        print("[OUTPUT] writing to dir " + sim_results_dir_root)
        print(sniper_command % {**locals(), **config})
        os.system(sniper_command % {**locals(), **config})
        
        os.system('mv *.trace %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.out %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.log %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv dramsim** %(sim_results_dir)s' % {**locals(), **config})


def run_sniper_gdb(bench):
    print("******************* Running sniper " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    sim_results_dir_root = 'sim-{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
    print("Simulation name: " + sim_results_dir_root)
    sim_results_dir_root = os.path.join(bench_path, sim_results_dir_root)
    os.makedirs(sim_results_dir_root)
    exe_command = benches[bench]['cmd']
    for r in benches[bench]['regions']:
        try: 
            if config['ncores'] != 10 and r['ncores'] != config['ncores']:
                continue
        except(KeyError):
            continue
        
        sim_results_dir = os.path.join(sim_results_dir_root, r['name'])
        os.makedirs(sim_results_dir)
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        
        print("[OUTPUT] writing to dir " + sim_results_dir_root)
        print(sniper_command_gdb % {**locals(), **config})
        os.system(sniper_command_gdb % {**locals(), **config})
        
        os.system('mv *.trace %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.out %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.log %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv dramsim** %(sim_results_dir)s' % {**locals(), **config})
    os.system('rm -rf %(sim_results_dir_root)s' % {**locals(), **config})
        
def run_region(bench):
    print("******************* Running regions " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'regions')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    exe_command = benches[bench]['cmd']
    for r in benches[bench]['regions']:
        try: 
            ncores = r['ncores']
            if config['ncores'] != 10 and ncores != config['ncores']:
                continue
        except(KeyError):
            continue
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        pinplay_log = os.path.join(results_dir, r['name'])
        os.system('rm -f %s*' % pinplay_log)
        print(region_command % {**locals(), **config})
        os.system(region_command % {**locals(), **config})
        os.system('mv foo.event_icount* %s' % results_dir)
        
def run_roi_icount(bench):
    print("******************* Running roi icount " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'roi')
    if os.path.exists(results_dir):
        os.system('rm -rf %s' % results_dir)
    os.makedirs(results_dir)
    exe_command = benches[bench]['cmd']
    pinplay_log = os.path.join(results_dir, 'roi')
    print(roi_icount_command % {**locals(), **config})
    os.system(roi_icount_command % {**locals(), **config})
    os.system('mv foo.event_icount* %s' % results_dir)
        
import sys

for bench in test_set:
    argv = sys.argv[1]
    if (argv == 'native'):
        run_native(bench)
    if (argv == 'sniper'):
        run_sniper(bench)
    if (argv == 'sniper-gdb'):
        run_sniper_gdb(bench)
    if (argv == 'region'):
        run_region(bench)
    if (argv == 'icount'):
        run_roi_icount(bench)
