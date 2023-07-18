###### onnxruntime
./build.sh --config Release --build_shared_lib --parallel --skip_tests


### test warmup events

$SDE_BUILD_KIT/sde -t sde-global-event-icounter.so -prefix foo -thread_count 10 -control warmup-start:address:chain+0x3229:count3981422787:global -control start:address:chain+0x3229:count4329326580:global -control stop:address:chain+0x3229:count4456164370:global -controller_log 1 -- ./chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t 10


### sniper parsec
export LD_LIBRARY_PATH=/home/joydong/Desktop/spec/parsec-benchmark/pkgs/libs/hooks/inst/amd64-linux.gcc-hooks/lib
/home/joydong/Desktop/spec/sniper/run-sniper        -n 10      -v -sprogresstrace:10000000 -gtraceinput/timeout=2000 -gscheduler/type=static -cicelake_s --no-cache-warming -ssimuserroi --roi-script --trace-args="-pinplay:control start:address:__parsec_roi_begin:bcast" --trace-args="-pinplay:control stop:address:__parsec_roi_end:bcast" -ggeneral/inst_mode_init=fast_forward -gperf_model/fast_forward/oneipc/include_memory_latency=true -d /home/joydong/Desktop/spec/parsec-benchmark/pkgs/apps/blackscholes/sim/blackscholes-simlarge-20230715/  -- "../inst/amd64-linux.gcc-hooks/bin/blackscholes 9 ../run/in_64K.txt ../run/prices.txt" 2>&1 | tee sniper.out



--maxthreads=10 --trace-dir="/mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-10-20230629154100/simulation/r1_1"

-n 10        -v -sprogresstrace:10000000 -gtraceinput/timeout=2000 -gscheduler/type=static -cicelake_s --trace-args="-sniper:flow 1000" -ssimuserroi --roi-script --trace-args="-pinplay:control start:address:chain+0x3229:count4329326580:global" --trace-args="-pinplay:control stop:address:chain+0x3229:count4456164370:global" -gperf_model/fast_forward/oneipc/interval=100 -ggeneral/inst_mode_init=cache_only --cache-only -gperf_model/fast_forward/oneipc/include_memory_latency=true -d /mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-10-20230629154100/simulation/r1        -- "./chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t 10"

## gen bbv
/home/joydong/Desktop/spec/looppoint/tools/gen_concat_vectors /mnt/sda/spec/genomicsbench/benchmarks/dbg/custom-chain-0-test-passive-10-default/dbg.0_795572.Data/dbg.0_795572.global.bb 10

### gen cluster
/home/joydong/Desktop/spec/looppoint/tools/sde-external-9.14.0-2022-10-25-lin/pinplay-scripts/sde_pinpoints.py --pintool=sde-global-looppoint.so --global_regions --pccount_regions --cfg /mnt/sda/spec/genomicsbench/benchmarks/chain/chain.cfg --whole_pgm_dir /mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-10-default/whole_program.0 -S 10000000000 --warmup_factor=1 --maxk=50 --dimensions=100 --append_status -s --simpoint_options=" -dim 100 -coveragePct 1.0 -maxK 50 " -- "./chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out -t 10"


/home/joydong/Desktop/spec/looppoint/tools/sde-external-9.14.0-2022-10-25-lin/pinplay-scripts/sde_pinpoints.py --pintool=sde-global-looppoint.so --global_regions --pccount_regions --cfg /mnt/sda/spec/genomicsbench/benchmarks/chain/chain.cfg --whole_pgm_dir /mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-10-20230629154100/whole_program.0 -S 10000000000 --warmup_factor=2 --maxk=50 --dimensions=100 --append_status -s --simpoint_options= -dim 100 -coveragePct 1.0 -maxK 50  


############################################################
########### Run Loop Point commands ########################
############################################################
./looppoint/run-looppoint.py -c $LOOPPOINT_CFG -n 10 --force --no-validate --reuse-profile -a icelake_s --pin-hook --warmup-factor=1 --roi-length=1000000000 --no-flowcontrol
############################################################
########### Run Sniper commands ############################
############################################################
./sniper/record-trace --roi -f 50000000000 -d 1000000000 -o results/bsw/trace.sift -- ./genomicsbench/benchmarks/bsw/bsw -pairs genomicsbench/input-datasets/bsw/large/bandedSWA_SRR7733443_1m_input.txt -t 1 -b 512

/home/joydong/Desktop/snipersim/run-sniper --roi -n 10 -c icelake_s -sprogresstrace:10000000 --no-cache-warming  -- ../pr -f ../wikipedia-20070206/wikipedia-20070206.mtx -n 1 | tee sniper.out

./vnsniper/run-sniper -c icelake -n 4 --traces=results/bsw/trace.sift --cache-only
###################################################################
############ Run genomics bench commands ##########################
###################################################################
## fmi
./genomicsbench/benchmarks/fmi/fmi ./genomicsbench/input-datasets/fmi/broad ./genomicsbench/input-datasets/fmi/large/SRR7733443_10m_1.fastq 512 19 1

## bsw
/usr/bin/time -v 
heaptrack ./bsw -pairs ../../input-datasets/bsw/large/bandedSWA_SRR7733443_1m_input.txt -t 1 -b 512
./pin/pin -t pin/source/tools/ManualExamples/obj-intel64/inscount2.so -- ./genomicsbench/benchmarks/bsw/bsw -pairs genomicsbench/input-datasets/bsw/large/bandedSWA_SRR7733443_1m_input.txt -t 1 -b 512

## phmm
export LD_LIBRARY_PATH=$PWD/genomicsbench/tools/GKL/build/native/:$LD_LIBRARY_PATH
./genomicsbench/benchmarks/phmm/phmm -f ./genomicsbench/input-datasets/phmm/large/large.in -t 1

## dbg
./genomicsbench/benchmarks/dbg/dbg ./genomicsbench/input-datasets/dbg/large/ERR194147-mem2-chr22.bam chr22:0-50818468 ./genomicsbench/input-datasets/dbg/large/Homo_sapiens_assembly38.fasta 1


## chain
./genomicsbench/benchmarks/chain/chain -i ./genomicsbench/input-datasets/chain/large/c_elegans_40x.10k.in -o ./genomicsbench/input-datasets/chain/large/c_elegans_40x.10k.out

/mnt/sda/spec/looppoint/tools/sde-external-9.14.0-2022-10-25-lin/pinplay-scripts/sde_pinpoints.py --delete --mode mt --sdehome=/mnt/sda/spec/looppoint/tools/sde-external-9.14.0-2022-10-25-lin -control start:address:pin_hook_init,stop:address:pin_hook_fini --cfg /mnt/sda/spec/genomicsbench/benchmarks/chain/chain.cfg --log_options "-start_address main -log:fat  -log:mp_atomic 0 -log:mp_mode 0 -log:strace -log:basename /mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-10-20230627165414/whole_program.0/chain.0" --replay_options="-replay:strace" -l

/mnt/sda/spec/looppoint/tools/sde-external-9.14.0-2022-10-25-lin/sde -log -xyzzy  -log:mt 1 -log:compressed bzip2 -log:syminfo -log:pid -start_address main -log:fat  -log:mp_atomic 0 -log:mp_mode 0 -log:strace -log:basename /mnt/sda/spec/genomicsbench/benchmarks/chain/custom-chain-0-test-passive-20-20230618212134/whole_program.0/chain.0 -- ./chain -i ../../input-datasets/chain/large/c_elegans_40x.10k.in -o ../../input-datasets/chain/large/c_elegans_40x.10k.out


## poa
./genomicsbench/benchmarks/poa/poa -s ./genomicsbench/input-datasets/poa/large/input.fasta -t 1

# kmer-cnt
./genomicsbench/benchmarks/kmer-cnt/kmer-cnt --reads ./genomicsbench/input-datasets/kmer-cnt/large/Loman_E.coli_MAP006-1_2D_50x.fasta --config ./genomicsbench/tools/Flye/flye/config/bin_cfg/asm_raw_reads.cfg --threads 1 --debug

# pileup
./genomicsbench/benchmarks/pileup/pileup ./genomicsbench/input-datasets/pileup/large/HG002_prom_R941_guppy360_2_GRCh38_ch20.bam chr20:1-64444167 1 > ./genomicsbench/input-datasets/pileup/large/pileup.txt

# grm
./genomicsbench/benchmarks/grm/2.0/build_dynamic/plink2 --maf 0.01 --pgen ./genomicsbench/input-datasets/grm/large/chr1_phase3.pgen --pvar ./genomicsbench/input-datasets/grm/large/chr1_phase3.pvar --psam ./genomicsbench/input-datasets/grm/large/phase3_corrected.psam --make-grm-bin --out ./genomicsbench/input-datasets/grm/large/grm --threads 1