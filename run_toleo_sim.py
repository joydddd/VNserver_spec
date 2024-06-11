#!/usr/bin/python3

import os
import datetime

SPEC_ROOT = os.getcwd()
onnx_set = ['3dunet', 'resnet']
genome_set = ['fmi', 'fmi-l', 'bsw', 'bsw-l', 'dbg', 'dbg-s', 'chain', 'chain-m', 'kmer-cnt', 'kmer-cnt-s', 'pileup', 'pileup-s', 'bsw-s']
graph_set = ['pr', 'pr-kron', 'pr-kron-s','pr-kron-2', 'pr_spmv', 'sssp-road', 'sssp-twitter', 'bfs-kron', 'bfs-web', 'bfs-road', 'bfs-twitter', 'bc', 'cc', 'cc_sv', 'tc']
llama_set = ['llama-8', 'llama-5']
redis_set = ['redis-test', 'redis-5k', 'redis-5kw', 'redis-multi-p', 'redis-5kw-1']
memcached_set = ['memcached-test', 'memcached-1', 'memcached-2']
mysql_set = ['mysql-test', 'mysql-1']
hyrise_set = ['hyrise', 'hyrise-1', 'hyrise-2']

sim_test = ['bsw-s', 'pr-kron-s'] # small test cases for testing simulators
submission_set = ['bsw', 'fmi', 'chain', 'dbg-s', 'pileup-s', 'pr-kron', 'bfs-twitter', 'sssp-road', 'llama5']

genomics_bench = ['fmi', 'bsw', 'bsw-s', 'dbg-s', 'chain', 'pileup-s']
gapbs_bench = ['pr-kron-s', 'pr-kron', 'sssp-road', 'bfs-twitter']
llama2_bench = ['llama-8', 'llama-5']
db_bench = ['hyrise', 'mysql-test', 'memcached-test']

test_set = sim_test

config = {}
# config['simulator'] = 'vnsniper'
config['simulator'] = 'sniper-toleo'
config['regions'] = None;
config['abort_after_roi'] = ''
config['port'] = 9856
config['stats_period'] = 1000000




# arch_list = ['zen4_s']
arch_list = ['zen4_cxl']
# arch_list = ['zen4_vn']
# arch_list = ['zen4_no_freshness']
# arch_list = ['zen4_no_dramsim']
# arch_list = ['zen4_cxl_invisimem']

# arch_list = ['zen4_cxl', 'zen4_vn', 'zen4_no_freshness', 'zen4_cxl_invisimem']
config['ncores'] = 32


# arch_list = ['zen4_cxl_11']
# arch_list = ['zen4_no_dramsim_11']
# arch_list = ['zen4_vn_11', 'zen4_no_freshness_11']
# arch_list = ['zen4_invisimem_11']
# config['ncores'] = 11


# config['arch'] = 'coaxial_s'
# config['ncores'] = 12

# config['arch'] = 'icelake_s'
# config['arch'] = 'icelake_cxl'
# config['arch'] = 'icelake_vn'
# config['ncores'] = 10


arch_ncores = {
    'zen4_s'            : 32,
    'zen4_cxl'          : 32,
    'zen4_vn'           : 32,
    'zen4_no_freshness' : 32,
    'zen4_no_dramsim'   : 32,
    'zen4_cxl_invisimem': 32,
    'zen4_cxl_11'       : 11,
    'zen4_vn_11'        : 11,
    'zen4_no_freshness_11': 11,
    'zen4_no_dramsim_11': 11,
    'zen4_invisimem_11' : 11,
    'coaxial_s'         : 12,
    'icelake_s'         : 10,
    'icelake_cxl'       : 10,
    'icelake_vn'        : 10
}

G1 = 1000000000 # 1bilion
G10 = (G1*10)
M100 = 100000000 # 100 million
M1 = 1000000 # 1 million
M10 = (M1 * 10) # 10 million

################################### Overwrite from cmd arguments ###################################

import argparse

parser = argparse.ArgumentParser(description='Run Toleo Simulation')
parser.add_argument('mode', type=str, help='Mode to run the benchmarks. Options: native, region, icount, sniper, memtier')
parser.add_argument('memtier_mode', type=str, nargs='*', help='Mode to run the benchmarks. Options: load, test')
parser.add_argument('--bench', type=str, nargs='*', help='Benchmarks to run. Options: all, genomicsbench, sim_test or <test name>. run ./run_toleo_sim.py print-bench to print all available test cases')
parser.add_argument('--sim', type=str, help='Simulator to run the benchmarks. --sim <simulator name> (default sniper-toleo)')
parser.add_argument('--arch', type=str, nargs='*', help='Architecture to run the benchmarks. Options: zen4_cxl, zen4_vn, zen4_no_freshness, zen4_cxl_invisimem etc.')
parser.add_argument('-r','--region', type=str, nargs='*', help='Regions to run the benchmarks. Options: r1, r2, rs1-t32, etc.')
parser.add_argument('-a', '--abort_after_roi', action='store_true', help='Abort after ROI')
parser.add_argument('-p', '--port', type=int, help='Port number for db workloads')



args = parser.parse_args()
if args.mode == "print-bench":
    print("genomicsbench: ", genomics_bench)
    print("graphbench: ", gapbs_bench)
    print("llama2bench: ", llama2_bench)
    print("dbbench: ", db_bench)
    print("(default) sim_test -- Small tests cases meant for simulator debugging", sim_test)
    exit(0)
if args.bench:
    test_set = args.bench
    if "sim_test" in test_set:
        test_set.remove("sim_test")
        test_set.extend(sim_test)
    if "genomicsbench" in test_set:
        test_set.remove("genomicsbench")
        test_set.extend(genomics_bench)
    if "graphbench" in test_set:
        test_set.remove("graphbench")
        test_set.extend(gapbs_bench)
    if "llama2bench" in test_set:
        test_set.remove("llama2bench")
        test_set.extend(llama2_bench)
    if "dbbench" in test_set:
        test_set.remove("dbbench")
        test_set.extend(db_bench)
    if "all" in test_set:
        test_set.remove("all")
        test_set.extend(genomics_bench + gapbs_bench + llama2_bench + db_bench)
if args.arch:
    arch_list = args.arch
    config['ncores'] = arch_ncores[args.arch[0]]
if  args.sim:
    config['simulator'] = args.sim
if args.region:
    config['regions'] = args.region
if args.abort_after_roi:
    config['abort_after_roi'] = ':abort'
if args.port:
    config['port'] = args.port

################################### Overwrite from cmd arguments ###################################


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
                {'name': 'r2', 'ff_icount' : 42855540806, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : 62904630178, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                # {'name': 'r2-t32', 'ff_icount' : 122904630178, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                {'name': 'rs1-t32', 'ff_icount' : 62904630178, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                ]
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
    'regions': [
                # {'name': 'r1', 'ff_icount' : 89081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                # {'name': 'r2', 'ff_icount' : 49081946856, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'rs1-t32', 'ff_icount' : 49081946856, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                ]
}

benches['bsw-l'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/large/bandedSWA_SRR7733443_1m_input.txt  -t %(ncores)s -b 512' % config,
    # pin_hook_init global icount: 23,484,072,677
    # pin_hook_fini global icount: 721,547,029,143 // 698,062,956,466
    'regions': [
                # {'name': 'r1-t32', 'ff_icount' : 223568924357, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'rs1-t32', 'ff_icount' : 223568924357, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                # {'name': 'r2-t32', 'ff_icount': 423568924357, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ]
}


benches['bsw-s'] = {
    'cmd' :  './bsw -pairs ../../input-datasets/bsw/small/bandedSWA_SRR7733443_100k_input.txt  -t %(ncores)s -b 512' % config,
    # 'regions': [{'name': 'r1-t32', 'ff_icount' : 3238814760, 'warmup_icount' : M1*32, 'sim_icount' : M1*32, 'ncores': 32 }]
    'regions': [{'name': 'r2-t32', 'ff_icount' : 1238814760, 'warmup_icount' : M10*32, 'sim_icount' : M10*32, 'ncores': 32 }]
}

benches['dbg'] = {
    'cmd' : './dbg ../../input-datasets/dbg/large/ERR194147-mem2-chr22.bam chr22:0-50818468 ../../input-datasets/dbg/large/Homo_sapiens_assembly38.fasta %(ncores)s' % config,
    # pin_hook_init global icount: 135,442,369,317
    # pin_hook_fini global icount: 2,252,177,293,572 // 2,116,734,924,255
    'regions': [{'name': 'r1', 'ff_icount' : 1116734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 516734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r3', 'ff_icount' : 1516734924255, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : 835447539618, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                # {'name': 'r2-t32', 'ff_icount': 1635447539618, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ]
}

benches['dbg-s'] = {
    'cmd' : './dbg ../../input-datasets/dbg/large/ERR194147-mem2-chr22.bam chr22:0-20818468 ../../input-datasets/dbg/large/Homo_sapiens_assembly38.fasta %(ncores)s' % config,
    'regions': [
                {'name': 'rs1-t32', 'ff_icount': 107329187339, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 }]
}

benches['chain'] = {
    'cmd' : './chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t %(ncores)s' % config,
    # pin_hook_init global icount: 897,270,215,617
    # pin_hook_fini global icount: 1,337,813,610,738 // 440,543,395,121
    'regions': [
                {'name': 'r1', 'ff_icount' : 230543395121, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 130543395121, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r1-t32', 'ff_icount' : 140593939208, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 340593939208, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'rs1-t32', 'ff_icount': 140593939208, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 }
                ]
}


benches['chain-m'] = {
    'cmd' : './chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in_100m -o ../../input-datasets/chain/large/c_elegans_40x.100m.out -t %(ncores)s' % config,
}

benches['kmer-cnt'] = {
    'cmd' : './kmer-cnt --reads ../../input-datasets/kmer-cnt/large/Loman_E.coli_MAP006-1_2D_50x.fasta --config ../../tools/Flye/flye/config/bin_cfg/asm_raw_reads.cfg --threads %(ncores)s' % config,
    'regions': [
                # {'name': 'r1-t32', 'ff_icount' : 7780355253, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'rs1-t32', 'ff_icount' : 27780355253, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                ],
    'extra-threads': 300,
    'scheduler' : 'pinned'
}

benches['kmer-cnt-s'] = {
    'cmd' : './kmer-cnt --reads ../../input-datasets/kmer-cnt/small/Loman_E.coli_MAP006-1_2D_50x_1000.fasta --config ../../tools/Flye/flye/config/bin_cfg/asm_raw_reads.cfg --threads %(ncores)s' % config,
    'regions': [],
    'extra-threads': 100,
    'scheduler' : 'pinned'
}


benches['pileup'] = {
    'cmd' : './pileup ../../input-datasets/pileup/large/HG002_prom_R941_guppy360_2_GRCh38_ch20.bam chr20:1-64444167 %(ncores)s ' % config,
    # pin_hook_init global icount:14,246,308
    # pin_hook_fini global icount: 1,050,781,289,380 // 1,050,767,043,072
    'regions': [
                {'name': 'r1', 'ff_icount' : 250767043072, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                # {'name': 'r2', 'ff_icount' : 650767043072, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                # {'name': 'rs1-t32', 'ff_icount' : G1*300, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
               ]
}

benches['pileup-s'] = {
    'cmd' : './pileup ../../input-datasets/pileup/large/HG002_prom_R941_guppy360_2_GRCh38_ch20.bam chr20:1-14444167 %(ncores)s ' % config,
    'regions': [
                {'name': 'rs1-t32', 'ff_icount' : 105498345510, 'warmup_icount' : 32*M10, 'sim_icount' : 32*M100, 'ncores': 32 },
                {'name': 'r1-t32', 'ff_icount' : 105498345510, 'warmup_icount' : 32*M100, 'sim_icount' : 32*G1, 'ncores': 32 },
                ]
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
                {'name': 'r1-t32', 'ff_icount' : 40111837215, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount': 80111837215, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },  
                {'name': 'rs1-t32', 'ff_icount' : 40111837215, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 }
                ]
}

# same as pr-kron. Just for running a second instance. 
benches['pr-kron-2'] = { 
    'cmd' : '../../pr -f ../../benchmark/graphs/kron-g27.sg -n 1',
    # t = 32
    # pin_hook_init global icount: 1,085,882,166
    # pin_hook_fini global icount: 125,263,751,069 // 124,177,868,903
    'regions': [
                # {'name': 'r1-t32', 'ff_icount' : 40111837215, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                # {'name': 'r2-t32', 'ff_icount': 80111837215, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },  
                {'name': 'rs1-t32', 'ff_icount' : 40111837215, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 }
                ]
}

benches['pr-kron-s'] = {
    'cmd' : '../../pr -f ../../benchmark/graphs/kron-g22.sg -n 1',
    'regions': [{'name': 'r1-t11', 'ff_icount' : 838926162, 'warmup_icount' : M1*11, 'sim_icount' : M1*11, 'ncores': 11 },
                {'name': 'r2-t11', 'ff_icount' : 838926162, 'warmup_icount' : M10*11, 'sim_icount' : M10*11, 'ncores': 11 },
                {'name': 'r1-t32', 'ff_icount' : 2068478955, 'warmup_icount' : M1*32, 'sim_icount' : M1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount' : 1068478955, 'warmup_icount' : M10*32, 'sim_icount' : M10*32, 'ncores': 32 }
                ]
}

benches['pr_spmv'] = {
    'cmd' : '../../pr_spmv -f ../../webbase-2001/webbase-2001.mtx -n 1',
    # pin_hook_init global icount: 4585059346044
    # pin_hook_fini global icount: 4752972186227 // 167,912,840,183
    'regions': [{'name': 'r1', 'ff_icount' : 107912840183, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 57912840183, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}


benches['bfs-web'] = {
    'cmd' : '../../bfs -f ../../benchmark/graphs/web.sg -n 1',
}

benches['bfs-kron'] = {
    'cmd' : '../../bfs -f ../../benchmark/graphs/kron-g27.sg -n 1',
    'regions':[
        {'name': 'roi', 'ncores': 32 }
    ],
}

benches['bfs-road'] = {
    'cmd' : '../../bfs -f ../../benchmark/graphs/road.sg -n 1',
}

benches['bfs-twitter'] = {
    'cmd' : '../../bfs -f ../../benchmark/graphs/twitter.sg -n 1',
    'ff-mode': 'cache_only',
    # 'ff-model': 'oneipc',
    'regions':[
        {'name': 'rs1-t32', 'ff_icount' : M10, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
        {'name': 'roi', 'ncores': 32 }
    ],
}


benches['sssp-road'] = {
    'cmd' : '../../sssp -f ../../benchmark/graphs/road.wsg -d50000 -n 1',
    'regions':[
        {'name': 'rs1-t32', 'ff_icount' : 1067946919, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
    ]
}


benches['sssp-twitter'] = {
    'cmd' : '../../sssp -f ../../benchmark/graphs/twitter.wsg -d2 -n 1',
    'regions':[
        {'name': 'rs1-t32', 'ff_icount' : 6187789171, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
    ]
}

benches['bc'] = {
    'cmd' : '../../bc -f ../../GAP-road/GAP-road.mtx -n 1',
}

benches['cc'] = {
    'cmd' : '../../cc -f ../../benchmark/graphs/twitter.sg -n1',
    'regions':[
        {'name': 'rs1-t32', 'ff_icount' : 1012802711, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
    ]
}

benches['cc_sv'] = {
    'cmd' : '../../cc_sv -f ../../webbase-2001/webbase-2001.mtx -n 1',
    # pin_hook_init global icount: 4584898946423
    # pin_hook_fini global icount: 4684589336834 // 99,690,390,411
    'regions': [{'name': 'r1', 'ff_icount' : 69690390411, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 },
                {'name': 'r2', 'ff_icount' : 39690390411, 'warmup_icount' : 1000000000, 'sim_icount' : 10000000000 }]
}

benches['tc'] = {
    'cmd' : '../../tc -f ../../benchmark/graphs/kronU.sg -n 1',
}

benches['llama-8'] = {
    'cmd' : '../../run ../../model/llama2_7b.bin -z ../../tokenizer.bin -n 8',
    'regions': [
                # {'name': 'rs1-t32', 'ff_icount' : 21492126225, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                {'name': 'r1-t32', 'ff_icount' : M10*32, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                ]
}

benches['llama-5'] = {
    'cmd' : '../../run ../../model/llama2_7b.bin -z ../../tokenizer.bin -n 5',
    'regions': [{'name': 'rs1-t32', 'ff_icount' : 15561094057, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                ]
}

benches['redis-test'] = {
    'cmd' : '../../src/redis-server ./redis.conf --server-cpulist 1-%(ncores)s',
    
    'loading_cmd': './memtier_benchmark --ratio=1:0 -R -t 10 -c 50 --requests=allkeys --key-pattern=P:P  --key-maximum=100000000', ## Database generation command. Produce a dump.rdb file in the running directory.
    
    'workload_cmd': './memtier_benchmark --ratio=1:10 -R -t 4 -c 50 --requests=10000 --key-pattern=G:G  --key-maximum=100000000 --wait-for-server-load', ## workload generation command 
    'regions': [
                ]
}

benches['redis-5k'] = {
    'cmd' : '../../src/redis-server ./redis.conf --loglevel debug --port %(port)s',
    'ff-model': 'none', 
    'regions': [
                # {'name': 'rs1-t32', 'ff_icount' : 54700240978, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                {'name': 'r1-t32', 'ff_icount' : 24700240978, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ],
    'workload_cmd': './memtier_benchmark --ratio=1:10 -R -t 4 -c 50 --requests=50000 --key-pattern=G:G  --key-maximum=100000000 --wait-for-server-load --port %(port)s', ## workload generation command 
}


benches['redis-5kw'] = {
    'cmd' : '../../src/redis-server ./redis.conf --io-threads %(app_threads)d --loglevel debug --port %(port)s',
    'no-oversubscribe': True, 
    'ff-model': 'none', 
    'extra-threads': 7, # bio_close_file, bio_aof, bio_lazy_free
    'regions':  [
                {'name': 'r1-t11', 'ff_icount' : 8699635780, 'warmup_icount' : M100*11, 'sim_icount' : G1*11, 'ncores': 11 },
                {'name': 'roi', 'ncores': 11 },
                {'name': 'rs1-t11', 'ff_icount' : 8699635780, 'warmup_icount' : M10*11, 'sim_icount' : M100*11, 'ncores': 11 },
                {'name': 'r1-t32', 'ff_icount' : 43454587818, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 }
                ],
    'workload_cmd': './memtier_benchmark --ratio=1:0 -R -t 4 -c 50 --requests=5000 --key-pattern=G:G  --key-maximum=100000000 --wait-for-server-load --port %(port)s' , ## workload generation command 
}

benches['redis-5kw-1'] = benches['redis-5kw'] # to run multiple redis in parallel. 


# benches['redis-multi-p'] = {
#     'cmd' : '../../src/redis-server --multi-service 2'
#             ' ./redis.conf --port 6379 --server-cpulist 0-15 --loglevel debug --dbfilename dump.rdb' 
#             ' ./redis.conf --port 6380 --server-cpulist 16-31 --loglevel debug --dbfilename dump.rdb.1' % config,
#     'regions':  [
#                 ],
#     'workload_cmd': './memtier_benchmark --ratio=1:0 -R -t 4 -c 50 --requests=5000 --key-pattern=G:G  --key-maximum=100000000 --wait-for-server-load --port 6379'
#                     './memtier_benchmark --ratio=1:0 -R -t 4 -c 50 --requests=5000 --key-pattern=G:G  --key-maximum=100000000 --wait-for-server-load --port 6380'## workload generation command 
# }


benches['memcached-test'] = {
    # 'cmd' : '../../memcached -m 12288 -vv -t %(ncores)s --enable-shutdown' % config,
    'cmd' : '../../memcached -m 12288 -v -t %(app_threads)d --enable-shutdown -p %(port)s',
    'no-oversubscribe': True,
    'ff-model': 'none', 
    'scheduler' : 'static',
    'stats': 10000,
    'regions':  [
                {'name': 'rs1-t32', 'ff_icount' : 19266894630, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                {'name': 'rs2-t32', 'ff_icount' : 19266894630, 'warmup_icount' : M10*32, 'sim_icount' : M100*32/5, 'ncores': 32 },
                {'name': 'rs3-t32', 'ff_icount' : 19266894630, 'warmup_icount' : M10*32, 'sim_icount' : M10, 'ncores': 32 },
                {'name': 'r1-t32', 'ff_icount' : 19266894630, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'r2-t32', 'ff_icount' : 19266894630, 'warmup_icount' : M100*32, 'sim_icount' : G10*32, 'ncores': 32 },
                # {'name': 'roi', 'ncores': 32 }
                ],
    'extra-threads': 6, # maintenaince, crawler, lru_maintainer, logger, rebalance
    'loading_cmd': './memtier_benchmark --protocol=memcache_text --ratio=1:0 -R -t 10 -c 50 --requests=allkeys --key-pattern=P:P --key-maximum=100000000 --port %(port)s',
    'workload_cmd': ' ./memtier_benchmark --protocol=memcache_text --ratio=1:0 -R -t 4 -c 50 --requests=500000 --key-pattern=G:G --wait-for-server-load --key-maximum=100000000 --shutdown-server --port %(port)s'
}

benches['memcached-1'] = benches['memcached-test'] # for running multiple memcached at the same time

benches['memcached-2'] = benches['memcached-test'] # for running multiple memcached at the same time

benches['memcached-3'] = benches['memcached-test'] # for running multiple memcached at the same time


benches['mysql-test'] = {
    # 'pre-cmd': '../../usr/local/mysql/bin/mysqld --defaults-file=./my.cnf -P %(port)s --initialize-insecure',
    'pre-cmd': 'rm -rf ../../data; cp -r ../../data_100 ../../data',
    'cmd' : '../../usr/local/mysql/bin/mysqld --defaults-file=./my.cnf --port %(port)s --skip-mysqlx --debug',
    # 'post-cmd': 'rm  -rf ./data',
    # 'cmd': '../../usr/local/mysql/bin/mysqld --defaults-file=./my.cnf -P %(port)s --initialize-insecure', ##Create Server
    'regions':  [
                {'name': 'rs1-t32', 'ff_icount' : 0, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32 },
                {'name': 'r1-t32', 'ff_icount' : 0, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                ],
    'extra-threads': 50, # maintenaince, crawler, lru_maintainer, logger, rebalance
    'wl_path': '%s/mysql/tpcc-mysql' % SPEC_ROOT,
    'scheduler' : 'pinned',
    'ff-model': 'none', 
    

    'loading_cmd': '../usr/local/mysql/bin/mysqladmin -P %(port)s -u root create tpcc100; ../usr/local/mysql/bin/mysql -u root -P %(port)s tpcc100 < create_table.sql; ../usr/local/mysql/bin/mysql -u root -P %(port)s tpcc100 < add_fkey_idx.sql;',  # Create tables
    'loading_cmd': 'export LD_LIBRARY_PATH=$SPEC_ROOT/mysql/usr/local/mysql/lib:$LD_LIBRARY_PATH; ./load.sh tpcc100 100 %(port)s',
    # 'loading_cmd': ' ../usr/local/mysql/bin/mysqldump --all-databases -u root  > ../dump.sql', # export database to sql
    'loading_cmd': '../usr/local/mysql/bin/mysqladmin -u root --password="" shutdown -P %(port)s', # export database to sql
    'workload_cmd': 'export LD_LIBRARY_PATH=$SPEC_ROOT/mysql/usr/local/mysql/lib:$LD_LIBRARY_PATH; export PATH=$SPEC_ROOT/mysql/usr/local/mysql/bin:$PATH; ./tpcc_start -h127.0.0.1 -dtpcc100 -uroot -P %(port)s -p "" -w100 -c32 -r0 -l0 -q400 -#100'
}

benches['mysql-1'] = benches['mysql-test'].copy() # for running multiple mysql at the same time
benches['mysql-1']['pre-cmd'] = 'rm -rf ../../data-1; cp -r ../../data_100 ../../data-1'

benches['hyrise'] = {
     'cmd' : '../../build/hyriseBenchmarkTPCC -s 10 --clients 30 --cores 30 -w 100000000000 --scheduler --time 100000000000 -r 10000 --warmup-runs 200 --data_preparation_cores 30',  
    'ff-model': 'none', 
    'scheduler' : 'pinned',
    'regions':  [
                {'name': 'r1-t32', 'ff_icount' : 0, 'warmup_icount' : M100*32, 'sim_icount' : G1*32, 'ncores': 32 },
                {'name': 'rs1-t32', 'ff_icount' : 0, 'warmup_icount' : M10*32, 'sim_icount' : M100*32, 'ncores': 32  },
                {'name': 'roi', 'ncores': 32 }
                ],
    'extra-threads': 100, # maintenaince, crawler, lru_maintainer, logger, rebalance
}

benches['hyrise-1'] = benches['hyrise'].copy()
benches['hyrise-2'] = benches['hyrise'].copy()
# benches['hyrise-2']['cmd'] = '../../build/hyriseConsole tpch.sql'

###################### Sniper Commands ######################
sniper_command = '$SNIPER_ROOT/run-sniper       -n %(ncores)s     -v -sprogresstrace:10000000 -speriodic-stats:%(stats_period)s:2000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming -ssimuserwarmup%(abort_after_roi)s --roi-script --trace-args="-pinplay:control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global"  --trace-args="-pinplay:controller_log 1"  --trace-args="-pinplay:controller_olog %(sim_results_dir)s/pinplay_controller.log" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/model=oneipc -gperf_model/fast_forward/oneipc/include_memory_latency=false -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'

sniper_command_roi = '$SNIPER_ROOT/run-sniper       -n %(ncores)s     -v -sprogresstrace:10000000 -speriodic-stats:%(stats_period)s:2000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming --roi -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/model=oneipc -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out' # -gperf_model/fast_forward/oneipc/include_memory_latency=false

sniper_command_gdb = '$SNIPER_ROOT/run-sniper       -n %(ncores)s  --gdb-wait   -v -sprogresstrace:10000000 -speriodic-stats:%(stats_period)s:2000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming -ssimuserwarmup%(abort_after_roi)s --roi-script --trace-args="-pinplay:control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global"  --trace-args="-pinplay:controller_log 1"  --trace-args="-pinplay:controller_olog %(sim_results_dir)s/pinplay_controller.log" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/model=oneipc -gperf_model/fast_forward/oneipc/include_memory_latency=false -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'

sniper_command_roi_gdb = '$SNIPER_ROOT/run-sniper       -n %(ncores)s   --gdb-wait  -v -sprogresstrace:10000000 -speriodic-stats:%(stats_period)s:2000 -gtraceinput/timeout=2000 -gscheduler/type=static -gscheduler/pinned/quantum=10000 -c%(arch)s --no-cache-warming --roi -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/model=oneipc -d %(sim_results_dir)s -- "%(exe_command)s" 2>&1 | tee %(sim_results_dir)s/sniper.out'


region_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count %(nthreads)s -control precond:address:pin_hook_init,warmup-start:icount:%(ff_icount)d:global,start:icount:%(warmup_icount)d:global,stop:icount:%(sim_icount)d:global -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'

roi_icount_command = '$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count %(nthreads)s -control start:address:pin_hook_init,stop:address:pin_hook_fini -controller_log 1 -controller_olog %(pinplay_log)s-controller.log -- %(exe_command)s 2>&1 | tee %(pinplay_log)s.out'


native_commamd = '/usr/bin/time -v %(exe_command)s 2>&1 | tee %(output_path)s/sniper.out'
# native_commamd = 'gdb --args %(exe_command)s '

os.environ["SPEC_ROOT"] = SPEC_ROOT
os.environ["SDE_BUILD_KIT"] = os.path.join(SPEC_ROOT, 'sde')
os.environ["PINBALL2ELF"] =  os.path.join(SPEC_ROOT, 'pinball2elf')
os.environ["SNIPER_ROOT"] = os.path.join(SPEC_ROOT, config['simulator'])
os.environ["OMP_NUM_THREADS"] = str(config['ncores'])

onnx_model_path = os.path.join(SPEC_ROOT, 'onnxruntime/models')
genom_bench_path = os.path.join(SPEC_ROOT, 'genomicsbench/benchmarks')
gapbs_bench_path = os.path.join(SPEC_ROOT, 'gapbs/run')
llama2_bench_path = os.path.join(SPEC_ROOT, 'llama2.c/sim')
redis_bench_path = os.path.join(SPEC_ROOT, 'redis/run')
memcached_bench_path = os.path.join(SPEC_ROOT, 'memcached/run')
memtier_path = os.path.join(SPEC_ROOT, 'memtier_benchmark')
mysql_path = os.path.join(SPEC_ROOT, 'mysql/run')
hyrise_path = os.path.join(SPEC_ROOT, 'hyrise/run')


def run_native(bench):
    print("******************* Running native " + bench + "************************")
    path = config['bench_path']
    bench_path = os.path.join(path, bench)
    output_path = os.path.join(bench_path, 'native-run')
    os.chdir(bench_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if 'pre-cmd' in benches[bench]:
        print('[PRE-CMD]' + benches[bench]['pre-cmd'] % {**locals(), **config})
        os.system(benches[bench]['pre-cmd'] % {**locals(), **config})
    exe_command = benches[bench]['cmd'] % config
    print(native_commamd % {**locals(), **config})
    os.system(native_commamd % {**locals(), **config})
    if 'post-cmd' in benches[bench]:
        os.system(benches[bench]['post-cmd'] % {**locals(), **config})
        
def run_sniper(bench):
    print("******************* Running sniper " + bench + "************************")
    path = config['bench_path']
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    sim_results_dir_root = 'sim-{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
    sim_results_dir_root += config['arch']
    print("Simulation name: " + sim_results_dir_root)
    sim_results_dir_root = os.path.join(bench_path, sim_results_dir_root)
    os.makedirs(sim_results_dir_root)
    exe_command = benches[bench]['cmd'] % config
    for r in benches[bench]['regions']:
        try: 
            if config['ncores'] != 10 and r['ncores'] != config['ncores']:
                continue
        except(KeyError):
            continue
        if config['regions'] and r['name'] not in config['regions']:
            continue
        print("///// REGION: " + r['name'] + " /////")
        
        sim_results_dir = os.path.join(sim_results_dir_root, r['name'])
        os.makedirs(sim_results_dir)
        
        if 'pre-cmd' in benches[bench]:
            print('[PRE-CMD]' + benches[bench]['pre-cmd'] % {**locals(), **config})
            os.system(benches[bench]['pre-cmd'] % {**locals(), **config})
        
        print("[OUTPUT] writing to dir " + sim_results_dir_root)
        if r['name'] == 'roi':
            sniper_exe = sniper_command_roi % {**locals(), **config}
        else:
            ff_icount = r['ff_icount']
            warmup_icount = r['warmup_icount']
            sim_icount = r['sim_icount']
            sniper_exe = sniper_command % {**locals(), **config}
        if 'scheduler' in benches[bench]:
            sniper_exe = sniper_exe.replace('-gscheduler/type=static', '-gscheduler/type='+benches[bench]['scheduler'])
        if 'ff-mode' in benches[bench]:
            sniper_exe = sniper_exe.replace('-ggeneral/inst_mode_init=fast_forward', '-ggeneral/inst_mode_init='+benches[bench]['ff-mode'])
        if 'ff-model' in benches[bench]:
            print("WARINING : ff-model is set to " + benches[bench]['ff-model'])
            sniper_exe = sniper_exe.replace('-gperf_model/fast_forward/model=oneipc', '-gperf_model/fast_forward/model='+benches[bench]['ff-model'])
        print(sniper_exe)
        os.system(sniper_exe)
        
        os.system('mv *.trace %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.out %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.log %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv dramsim** %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.csv %(sim_results_dir)s' % {**locals(), **config})
        if 'post-cmd' in benches[bench]:
            os.system(benches[bench]['post-cmd'] % {**locals(), **config})


def run_sniper_gdb(bench):
    print("******************* Running sniper " + bench + "************************")
    path = config['bench_path']
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    sim_results_dir_root = 'sim-{date:%Y-%m-%d_%H:%M:%S}'.format( date=datetime.datetime.now() )
    sim_results_dir_root += config['arch']
    print("Simulation name: " + sim_results_dir_root)
    sim_results_dir_root = os.path.join(bench_path, sim_results_dir_root)
    os.makedirs(sim_results_dir_root)
    exe_command = benches[bench]['cmd'] % config
    for r in benches[bench]['regions']:
        try: 
            if config['ncores'] != 10 and r['ncores'] != config['ncores']:
                continue
        except(KeyError):
            continue
        print("///// REGION: " + r['name'] + " /////")
        if config['regions'] and r['name'] not in config['regions']:
            continue
        
        sim_results_dir = os.path.join(sim_results_dir_root, r['name'])
        os.makedirs(sim_results_dir)
        
        if 'pre-cmd' in benches[bench]:
            print('[PRE-CMD]' + benches[bench]['pre-cmd'] % {**locals(), **config})
            os.system(benches[bench]['pre-cmd'] % {**locals(), **config})
        print("[OUTPUT] writing to dir " + sim_results_dir_root)
        if r['name'] == 'roi':
            sniper_exe = sniper_command_roi_gdb % {**locals(), **config}
        else:
            ff_icount = r['ff_icount']
            warmup_icount = r['warmup_icount']
            sim_icount = r['sim_icount']
            sniper_exe = sniper_command_gdb % {**locals(), **config}
        if 'scheduler' in benches[bench]:
            sniper_exe = sniper_exe.replace('-gscheduler/type=static', '-gscheduler/type='+benches[bench]['scheduler'])
        if 'ff-mode' in benches[bench]:
            sniper_exe = sniper_exe.replace('-ggeneral/inst_mode_init=fast_forward', '-ggeneral/inst_mode_init='+benches[bench]['ff-mode'])
        if 'ff-model' in benches[bench]:
            print("WARINING : ff-model is set to " + benches[bench]['ff-model'])
            sniper_exe = sniper_exe.replace('-gperf_model/fast_forward/model=oneipc', '-gperf_model/fast_forward/model='+benches[bench]['ff-model'])
        print(sniper_exe)
        os.system(sniper_exe)
        
        os.system('mv *.trace %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.out %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.log %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.csv %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv dramsim** %(sim_results_dir)s' % {**locals(), **config})
        os.system('mv *.csv %(sim_results_dir)s' % {**locals(), **config})
        if 'post-cmd' in benches[bench]:
            os.system(benches[bench]['post-cmd'] % {**locals(), **config})
    os.system('rm -rf %(sim_results_dir_root)s' % {**locals(), **config})
        
def run_region(bench):
    print("******************* Running regions " + bench + "************************")
    path = config['bench_path']
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'regions')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    exe_command = benches[bench]['cmd'] % config
    for r in benches[bench]['regions']:
        try: 
            ncores = r['ncores']
            if config['ncores'] != 10 and ncores != config['ncores']:
                continue
        except(KeyError):
            continue
        if config['regions'] and r['name'] not in config['regions']:
            continue
        print("///// REGION: " + r['name'] + " /////")
        if 'pre-cmd' in benches[bench]:
            os.system(benches[bench]['pre-cmd'] % {**locals(), **config})
        ff_icount = r['ff_icount']
        warmup_icount = r['warmup_icount']
        sim_icount = r['sim_icount']
        pinplay_log = os.path.join(results_dir, r['name'])
        os.system('rm -f %s*' % pinplay_log)
        print(region_command % {**locals(), **config})
        os.system(region_command % {**locals(), **config})
        os.system('mv foo.event_icount* %s' % results_dir)
        if 'post-cmd' in benches[bench]:
            os.system(benches[bench]['post-cmd'] % {**locals(), **config})
        
def run_roi_icount(bench):
    print("******************* Running roi icount " + bench + "************************")
    path = config['bench_path']
    bench_path = os.path.join(path, bench)
    os.chdir(bench_path)
    results_dir = os.path.join(bench_path, 'roi')
    if os.path.exists(results_dir):
        os.system('rm -rf %s' % results_dir)
    os.makedirs(results_dir)
    if 'pre-cmd' in benches[bench]:
        os.system(benches[bench]['pre-cmd'] % {**locals(), **config})
    exe_command = benches[bench]['cmd'] % config
    pinplay_log = os.path.join(results_dir, 'roi')
    print(roi_icount_command % {**locals(), **config})
    os.system(roi_icount_command % {**locals(), **config})
    os.system('mv foo.event_icount* %s' % results_dir)
    if 'post-cmd' in benches[bench]:
        os.system(benches[bench]['post-cmd'] % {**locals(), **config})
    
def run_memtier(bench, load, test):
    print("******************* Running workload for" + bench + "************************")
    if 'wl_path' in benches[bench]:
        os.chdir(benches[bench]['wl_path'])
        os.system('pwd')
    else:
        os.chdir(memtier_path)
    if (load):
        print("LOADING......................................")
        print("cmd:" + benches[bench]['loading_cmd'] % config)
        os.system(benches[bench]['loading_cmd'] % config)
    if (test):
        print("TESTING......................................")
        print("cmd:" + benches[bench]['workload_cmd'] % config)
        os.system(benches[bench]['workload_cmd'] % config)
        
        
import sys
    
    

argv = args.mode
for bench in test_set:
    if 'stats' in benches[bench]:
        config['stats_period'] = benches[bench]['stats']
    config['nthreads'] = config['ncores']
    if 'extra-threads' in benches[bench]:
        if 'no-oversubscribe' in benches[bench] and benches[bench]['no-oversubscribe']:
            config['app_threads'] = config['ncores'] - benches[bench]['extra-threads']
        else: 
            config['nthreads'] += benches[bench]['extra-threads']
    config['bench_path'] = onnx_model_path if bench in onnx_set else genom_bench_path if bench in genome_set else gapbs_bench_path if bench in graph_set else redis_bench_path if bench in redis_set else memcached_bench_path if bench in memcached_set else mysql_path if bench in mysql_set else hyrise_path if bench in hyrise_set else llama2_bench_path
    if (argv == 'native'):
        run_native(bench)
    if (argv == 'region'):
        run_region(bench)
    if (argv == 'icount'):
        run_roi_icount(bench)
    if (argv == 'wl'):
        memtier_load = False
        memtier_test = False
        for arg in args.memtier_mode:
            if arg == 'load':
                memtier_load = True
            if arg == 'test':
                memtier_test = True
        run_memtier(bench, memtier_load, memtier_test)
    for arch in arch_list:
        config['arch'] = arch
        print("Arch: " + arch)
        if (argv == 'sniper'):
            run_sniper(bench)
        if (argv == 'sniper-gdb'):
            run_sniper_gdb(bench)
