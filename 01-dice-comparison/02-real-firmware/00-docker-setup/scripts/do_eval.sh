#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

config_loc="${DIR}/config.txt"

if [ ! -f $config_loc ]; then
	echo " Config file was not found! Exiting..."
	exit
fi


dice_script="${DIR}/dice_fuzz.sh"
dice_base="/opt/DICEFuzzBase"
p2im_script="${DIR}/p2im_fuzz.sh"
p2im_base="/opt/P2IMFuzzBase"

output_dir="/opt/results"
if [ ! -d $output_dir ]; then
	echo "No output directory mapped to docker container, expected $output_dir. Exiting..."
	exit
fi

# Config structure
# Time as one of Xs/Ym/Zh
# Cores to uses
# Iterations
# Target1
# ...
# TargetN

# Read Config
readarray -t config < $config_loc
targets=("${config[@]:3}")
timeout=("${config[@]:0:1}")
cores=("${config[@]:1:1}")
iterations=("${config[@]:2:1}")
target_string="${targets[*]}"


# Add the timeout to the configs
cd /opt/dice_configs
echo "timeout = $timeout" | tee -a *
cd -
cd /opt/p2im_configs
echo "timeout = $timeout" | tee -a *
cd -
# Run the fuzzers
bash $dice_script $cores $iterations $target_string
bash $p2im_script $cores $iterations $target_string

# Run the coverage scripts
python3 scripts/create_dice_cov.py --data-root $dice_base --cov-script /opt/scripts/cov.py --num-runs $iterations
python3 scripts/create_dice_cov.py --data-root $p2im_base --cov-script /opt/scripts/cov.py --num-runs $iterations

# collect results
mv $dice_base $output_dir
mv $p2im_base $output_dir

bash scripts/rename.sh $output_dir

chmod -R 777 $output_dir
