#!/usr/bin/python3

import os
import datetime

SPEC_ROOT = os.getcwd()
onnx_set = ['3dunet', 'resnet']
genome_set = ['fmi', 'bsw', 'dbg', 'chain', 'kmer-cnt', 'pileup']
test_set = ['bsw']
# test_set = ['resnet']


benches = {}
config  = {}
benches['resnet'] = {
    'cmd'   : '../../build/Linux/Release/onnx -r 1 -c 1 -x 10 ex/resnet50-v1-12.onnx -D',
    # pin_hook_init Global icount: 180325165538
    # pin_hook_fini Global icount: 359314218609// 178,989,053,071
    'regions' : [ {'name': 'r1', 'ff_icount' : 100989053071, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                  {'name': 'r2', 'ff_icount' : 50989053071, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000}]
}

benches['3dunet'] = {
    'cmd'   : '../../build/Linux/Release/onnx -r 1 -c 1 -x 10 ex/model.onnx -D',
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
    'cmd' : './fmi ../../input-datasets/fmi/broad ../../input-datasets/fmi/small/SRR7733443_1m_1.fastq 512 19 10',
    # pin_hook_init global icount: 11076996653
    # pin_hook_fini global icount: 173932537459 // 162,855,540,806
    'regions': [{'name': 'r1', 'ff_icount' : 82855540806, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }, 
                {'name': 'r2', 'ff_icount' : 42855540806, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['bsw'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/large/bandedSWA_SRR7733443_500k_input.txt  -t 10 -b 512',
    # pin_hook_init global icount: 11174244380
    # pin_hook_fini global icount: 170256191236 // 159,081,946,856
    'regions': [{'name': 'r1', 'ff_icount' : 89081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 49081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['dbg'] = {
    'cmd' : './dbg ../../input-datasets/dbg/large/ERR194147-mem2-chr22.bam chr22:0-50818468 ../../input-datasets/dbg/large/Homo_sapiens_assembly38.fasta 10',
    'regions': []
}

benches['chain'] = {
    'cmd' : './chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t 10',
    'regions': []
}

benches['kmer-cnt'] = {
    'cmd' : './kmer-cnt --reads ../../input-datasets/kmer-cnt/large/Loman_E.coli_MAP006-1_2D_50x.fasta --config ../../tools/Flye/flye/config/bin_cfg/asm_raw_reads.cfg --threads 10',
    'regions': []
}

benches['pileup'] = {
    'cmd' : './pileup ../../input-datasets/pileup/large/HG002_prom_R941_guppy360_2_GRCh38_ch20.bam chr20:1-64444167 10 ',
    'regions': []
}





config['arch'] = 'icelake_s'


###################### Sniper Commands ######################
sniper_command = '$SNIPER_ROOT/run-sniper        -n 10      -v -sprogresstrace:10000000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming -ssimuserwarmup --roi-script --trace-args="-pinplay:control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global"  --trace-args="-pinplay:controller_log 1"  --trace-args="-pinplay:controller_olog %(sim_results_dir)s/pinplay_controller.log" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/oneipc/include_memory_latency=true -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'

region_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count 10 -control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'

roi_icount_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count 10 -control start:address:pin_hook_init,stop:address:pin_hook_fini -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'


native_commamd = '/usr/bin/time -v %(exe_command)s 2>&1 | tee %(output_path)s/sniper.out'

os.environ["SPEC_ROOT"] = SPEC_ROOT
os.environ["SDE_BUILD_KIT"] = os.path.join(SPEC_ROOT, 'sde')
os.environ["PINBALL2ELF"] =  os.path.join(SPEC_ROOT, 'pinball2elf')
os.environ["SNIPER_ROOT"] = os.path.join(SPEC_ROOT, 'sniper')

onnx_model_path = os.path.join(SPEC_ROOT, 'onnxruntime/models')
genom_bench_path = os.path.join(SPEC_ROOT, 'genomicsbench/benchmarks')

def run_native(bench):
    print("******************* Running native " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path
    bench_path = os.path.join(path, bench)
    output_path = os.path.join(bench_path, 'native-run')
    os.chdir(bench_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    exe_command = benches[bench]['cmd']
    print(native_commamd % locals())
    os.system(native_commamd % locals())
        
def run_sniper(bench):
    print("******************* Running sniper " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    sim_results_dir_root = 'sim-{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
    sim_results_dir_root = os.path.join(bench_path, sim_results_dir_root)
    os.makedirs(sim_results_dir_root)
    arch = config['arch']
    exe_command = benches[bench]['cmd']
    for r in benches[bench]['regions']:
        sim_results_dir = os.path.join(sim_results_dir_root, r['name'])
        os.makedirs(sim_results_dir)
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        print(sniper_command % locals())
        print("[OUTPUT] writing to dir " + sim_results_dir_root)
        os.system(sniper_command % locals())
        os.system('mv *.trace %(sim_results_dir)s' % locals())
        os.system('mv *.out %(sim_results_dir)s' % locals())
        
def run_region(bench):
    print("******************* Running regions " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'regions')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    exe_command = benches[bench]['cmd']
    for r in benches[bench]['regions']:
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        pinplay_log = os.path.join(results_dir, r['name'])
        os.system('rm -f %s*' % pinplay_log)
        print(region_command % locals())
        os.system(region_command % locals())
        
def run_roi_icount(bench):
    print("******************* Running roi icount " + bench + "************************")
    path = onnx_model_path if bench in onnx_set else genom_bench_path
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'roi')
    if os.path.exists(results_dir):
        os.system('rm -rf %s' % results_dir)
    os.makedirs(results_dir)
    exe_command = benches[bench]['cmd']
    pinplay_log = os.path.join(results_dir, 'roi')
    print(roi_icount_command % locals())
    os.system(roi_icount_command % locals())
        
    

for bench in test_set:
    # run_native(bench)
    run_sniper(bench)
    # run_region(bench)
    # run_roi_icount(bench)