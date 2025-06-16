#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Please parse target directory as first argument"
	exit 1
fi
echo "Targetting $1"
# To allow for flexibility in the directory we run the fuzzer from, automaticall find the common directory for the python path env variable
dir_candidates=`find ./ -type d -name common`
array=(${dir_candidates// / })
ppath=""

if [ ${#array[@]} == 1 ]
then
	ppath=${array[0]}
	echo "Got target dir for pythonpath: $ppath"
else
	echo "Got many potential candidates for pythonpath. Looking for best fit"
	for element in "${array[@]}";
	do
		if [[ $element == *"04-finding-new-bugs/"* ]]
		then
			ppath=$element
			echo "Got fitting candidate: $ppath"
		fi
	done
fi

export PYTHONPATH=$ppath
fuzzware pipeline -n 10 --dma -c $1/hook_config.yml $1
