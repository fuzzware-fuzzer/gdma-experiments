#!/bin/sh

target_dir="build_cy8c_samples"
sample1_file="password.patch"
tag="cy8c-build-env"
filename="`basename $(pwd)`.tar.zstd"
idename="ModusToolbox_3.2.0.16028-linux-install.deb"
set -x
if [ ! -e $filename ] && [ $IMPORT_IMAGES ]  ; then
	src="`pwd`/../../../../docker-saves/02-extended-test-suite/$filename"
	if [ -e $src ] ; then
		cp $src .
	fi

fi

if [ ! -e $idename ] && [ ! $IMPORT_IMAGES ]  ; then
	src="`pwd`/../../../../ides/$idename"
	if [ -e $src ] ; then
		cp $src .
	fi

fi


rm -rf /tmp/$target_dir
mkdir /tmp/$target_dir
cp $sample1_file /tmp/$target_dir
cp build_samples.sh /tmp/$target_dir
if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then zstd -d $filename -T0 --stdout | docker load ; else docker build . -t $tag ; fi
docker run --rm -it -v /tmp/$target_dir:/opt/samples $tag
ls /tmp/$target_dir/output
cp /tmp/$target_dir/output/mtb-example-psoc6-uart-transmit-receive-dma.elf output
if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then docker save $tag | zstd -T0 > $filename ; fi
