#!/bin/bash

if [ "$#" -ne 2 ]; 
then
	echo "Usage TODO"
fi

experiment_base=$1
plot_dir=$2
dice_fuzz_base=""
p2im_fuzz_base=""

if [ -n "$(ls -A ${experiment_base}/DICEFuzzBase 2>/dev/null)" ]
then
	echo "Got $experiment_base/DICEFuzzBase"
	dice_fuzz_base="${experiment_base}/DICEFuzzBase"
else
	echo "Error"
	exit
fi

if [ -n "$(ls -A ${experiment_base}/P2IMFuzzBase 2>/dev/null)" ]
then
	echo "Got $experiment_base/P2IMFuzzBase"
	p2im_fuzz_base="${experiment_base}/P2IMFuzzBase"
else
	echo "Error"
	exit
fi

iterations=$(ls -1 $dice_fuzz_base/GPS-Receiver|wc -l)
echo $iterations
# Rename so the folder names match the config
fuzz_bases=($dice_fuzz_base $p2im_fuzz_base)
for dir in ${fuzz_bases[@]}
do
	cd $dir
	mv GPS-Receiver GPSReceiver
	mv Guitar-Pedal GuitarPedal
	mv MIDI-Synthesizer MIDISynthetizer
	mv Soldering-Station SolderingStation
	mv Stepper-Motor StepperMotor
	cd -
done


# start docker and mount the experiment base
docker run -v $dice_fuzz_base:/opt/DICEFuzzBase -v $p2im_fuzz_base:/opt/P2IMFuzzBase -it dice_tag /bin/bash -c "python3 /opt/scripts/create_dice_cov.py --data-root /opt/DICEFuzzBase --cov-script /opt/scripts/cov.py --num-runs ${iterations} && python3 /opt/scripts/create_dice_cov.py --data-root /opt/P2IMFuzzBase --cov-script /opt/scripts/cov.py --num-runs ${iterations}"


for dir in ${fuzz_bases[@]}
do
	cd $dir
	mv GPSReceiver GPS-Receiver
	mv GuitarPedal Guitar-Pedal
	mv MIDISynthetizer MIDI-Synthesizer 
	mv SolderingStation Soldering-Station
	mv StepperMotor Stepper-Motor
	cd -
done

# DICE 
out_file=out.txt
dice_dir=DICEFuzzBase
for i in `ls $experiment_base/$dice_dir`
do
	for u in $(seq 1 $runs )
	do
		mkdir -p $plot_dir/$dice_dir/$i/$u
		cp $experiment_base/$dice_dir/$i/$u/$out_file $plot_dir/$dice_dir/$i/$u
	done
done

# P2IM 
p2im_dir=P2IMFuzzBase
for i in `ls $experiment_base/$p2im_dir`
do
	for u in $(seq 1 $runs )
	do
		mkdir -p $plot_dir/$p2im_dir/$i/$u
		cp $experiment_base/$p2im_dir/$i/$u/$out_file $plot_dir/$p2im_dir/$i/$u
	done
done
