#!/bin/bash
num_parallel_procs=$1
experiment_repetition_count=$2
shift; shift;

target_list=$@
cur_run=1
# We run the target for the specified number of times to account for variance
( for run_no in `seq 1 $experiment_repetition_count`; do
    #export FUZZDIR=$project_base_name
    python3 /opt/P2IM-DMA-Emulation/DICE-Evaluation/ARM/Fuzzing/CreateBaseDir.py -B /opt/P2IMFuzzBase -R $run_no

    project_base_name="/opt/P2IMFuzzBase"

    for target in ${target_list[@]}; do
	cp /opt/P2IM-DMA-Emulation/p2im/fuzzing/templates/seeds/random $project_base_name/$target/$run_no/inputs/input.data
	cp /opt/p2im_configs/$target\_$cur_run.cfg $project_base_name/$target/$run_no/working_cov.cfg
	#echo "/opt/p2im_configs/$target\_$cur_run.cfg $project_base_name/$target/$run_no/working_cov.cfg"
	echo "FUZZDIR=$project_base_name timeout 10m python3 /opt/P2IM-DMA-Emulation/p2im/model_instantiation/fuzz.py -c /opt/p2im_configs/$target\_$cur_run.cfg "
    done
    cur_run=$(($cur_run+1))
    
#done ) | xargs -I{} --max-procs $num_parallel_procs -- echo "{}"
done ) | xargs -I{} --max-procs $num_parallel_procs -- bash -c "{}"
#python3 model_instantiation/fuzz.py -c mul_configs/GPSreceiver_1.cfg


