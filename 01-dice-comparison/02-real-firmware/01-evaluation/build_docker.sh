#!/bin/sh
tag="p2im_dice_eval"
target_dir="p2im_dice_results"
target_dir_full_path=$(realpath -s $target_dir)
dice_dir=DICEFuzzBase
p2im_dir=P2IMFuzzBase
final_results=../02-results
config=config.txt
out_file=out.txt
runs=$(sed '3q;d' ./config.txt)

rm -r ./$target_dir
mkdir -p ./$target_dir
echo "Replacing all previous data with zeros"
find ../02-results/ -name "out.txt" -exec bash -c 'echo 0 0 > {}' \;

docker build . -t $tag 
#docker run -it $tag 
docker run -it -v $target_dir_full_path:/opt/results  $tag 

# collect the fuzzing results
ls $target_dir

# DICE 
for i in `ls $target_dir/$dice_dir`
do
	for u in $(seq 1 $runs )
	do
		mkdir -p $final_results/$dice_dir/$i/$u
		cp $target_dir/$dice_dir/$i/$u/$out_file $final_results/$dice_dir/$i/$u
	done
done

# P2IM 
for i in `ls $target_dir/$p2im_dir`
do
	for u in $(seq 1 $runs )
	do
		mkdir -p $final_results/$p2im_dir/$i/$u
		cp $target_dir/$p2im_dir/$i/$u/$out_file $final_results/$p2im_dir/$i/$u
	done
done
