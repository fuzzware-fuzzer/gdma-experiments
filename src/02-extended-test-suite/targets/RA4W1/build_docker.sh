#!/bin/sh
target_dir="build_ra4w1_sample"
sample1_dir="ra4w1_serial_contiguous"
tag="ra4w1-build-env"
filename="`basename $(pwd)`.tar.zstd"

set -x
if [ ! -e $filename ] && [ $IMPORT_IMAGES ]  ; then
	src="`pwd`/../../../../docker-saves/02-extended-test-suite/$filename"
	if [ -e $src ] ; then
		cp $src .
	fi

fi

rm -rf /tmp/$target_dir
mkdir /tmp/$target_dir
cp -r $sample1_dir /tmp/$target_dir
cp build_samples.sh /tmp/$target_dir
if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then zstd -d $filename -T0 --stdout | docker load ; else docker build . -t $tag ; fi
docker run --rm -it -v /tmp/$target_dir:/opt/samples $tag
ls /tmp/$target_dir/output
mkdir output
cp /tmp/build_ra4w1_sample/ra4w1_serial_contiguous/Debug/dma_spi_ek_ra4w1_ep.elf output/ra4w1_serial_contiguous.elf
if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then docker save $tag | zstd -T0 > $filename ; fi
