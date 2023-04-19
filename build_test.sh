#!/bin/bash
SPEC_ROOT=/home/joydong/Desktop/snipersim/spec
SPEC_BUILD_INST=build_base_joy-m64.0000
SPEC_RUN_INST=run_base_refspeed_joy-m64.0000

fake_run_spec () {
    local TEST_BENCH="$1"
    cd $SPEC_ROOT/SPEC2017
	. ./shrc
	runcpu --fake --loose --size ref --tune base --config joy $TEST_BENCH
}

build_spec() {
    local TEST_BENCH="$1"

    ## Build binary using specmake
    cd SPEC2017
    . ./shrc
	go $1
	cd build/$SPEC_BUILD_INST
	
    if [ "$1" = "625.x264_s" ]; then
        specmake clean TARGET=x264_s > $SPEC_ROOT/log/$TEST_BENCH.build.log
        local BIN_FILENAME=`specmake TARGET=x264_s -j16 2>&1 | tee $SPEC_ROOT/log/$TEST_BENCH.build.log | grep -v -- "-c " | grep -o -- "-o \w*" | sed -E "s/-o //" | tee -a $SPEC_ROOT/log/spec_build.log;`
    else
        specmake clean > $SPEC_ROOT/log/$TEST_BENCH.build.log
        local BIN_FILENAME=`specmake -j16 2>&1 | tee $SPEC_ROOT/log/$TEST_BENCH.build.log | grep -v -- "-c " | grep -o -- "-o \w*" | sed -E "s/-o //" | tee -a $SPEC_ROOT/log/spec_build.log;`
    fi

    if [ "$1" = "648.exchange2_s" ]; then
        BIN_FILENAME=exchange2_s
    fi
    echo $BIN_FILENAME
    cp $BIN_FILENAME $SPEC_ROOT/spec_bin/${1}
}

gen_spec_run_cmd() {
    local TEST_BENCH="$1"
    cd SPEC2017
    . ./shrc
	go $1 run
    if [ -d $SPEC_ROOT/spec_bin/${1}_run ]; then rm -r $SPEC_ROOT/spec_bin/${1}_run; fi
    cp -r $SPEC_RUN_INST/. $SPEC_ROOT/spec_bin/${1}_run
    cp $SPEC_ROOT/spec_bin/${1} $SPEC_ROOT/spec_bin/${1}_run/app
    cd $SPEC_RUN_INST
    specinvoke -n | sed -E "s/..\/$SPEC_RUN_INST\/[[:alnum:]_.-]*/.\/app/" > $SPEC_ROOT/spec_bin/$1_run/run.sh
    chmod +x $SPEC_ROOT/spec_bin/$1_run/run.sh
}