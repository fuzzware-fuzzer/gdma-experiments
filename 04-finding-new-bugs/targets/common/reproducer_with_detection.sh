#!/bin/bash

if [ "$#" -ne 2 ]
then
	echo "Please parse target config and input"
	exit 1
fi
echo "Target Config $1"
echo "Target Input: $2"
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
fuzzware emu -d -v -c $1 $2
