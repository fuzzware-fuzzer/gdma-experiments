
#!/bin/sh
target_dir="build_lpc18xx_samples"
sample1_dir="periph_uart_sg"
tag="lpc18xx-build-env"
filename="`basename $(pwd)`.tar.zstd"
idename="mcuxpressoide-11.10.0_3148.x86_64.deb.bin"

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
cp -r $sample1_dir /tmp/$target_dir
cp build_samples.sh /tmp/$target_dir
if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then zstd -d $filename -T0 --stdout | docker load ; else docker build . -t $tag ; fi
docker run --rm -it -v /tmp/$target_dir:/opt/samples $tag 
ls /tmp/$target_dir/output
mkdir output
cp -r /tmp/$target_dir/output/$sample1_dir.elf output
if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then docker save $tag | zstd -T0 > $filename ; fi

