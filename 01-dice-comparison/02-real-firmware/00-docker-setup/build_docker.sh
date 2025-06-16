#!/bin/sh
tag="dice_tag"
target_dir="dice_eval"
filename="dice_docker.tar.zstd"
set -x

if [ ! -e $filename ] && [ $IMPORT_IMAGES ]  ; then
	src="`pwd`/../../../docker-saves/$filename"
	if [ -e $src ] ; then
		cp $src .
	fi
fi


if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then 
	zstd -d $filename -T0 --stdout | docker load ; 
else 
	docker build . -t $tag ; 
fi

if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then 
	docker save $tag | zstd -T0 > $filename ; 
fi
