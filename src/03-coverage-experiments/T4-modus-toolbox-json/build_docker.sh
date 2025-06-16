target_dir="build_mtb"
tag="mtb-build-env"
filename="`basename $(pwd)`.tar.zstd"

set -x
if [ ! -e $filename ] && [ $IMPORT_IMAGES ]  ; then
	src="`pwd`/../../../docker-saves/03-coverage-experiments/$filename"
	if [ -e $src ] ; then
		cp $src .
	fi

fi

rm -rf /tmp/$target_dir/output/*
mkdir -p /tmp/$target_dir/output/
chmod -R 777 /tmp/$target_dir/output
cp build_samples.sh /tmp/$target_dir
cp json.patch /tmp/$target_dir
if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then zstd -d $filename -T0 --stdout | docker load ; else docker build . -t $tag ; fi
docker run --rm -it -v /tmp/$target_dir:/opt/samples $tag
ls /tmp/$target_dir/output
cp -r /tmp/$target_dir/output/mtb-example-psoc6-uart-transmit-receive-dma.elf output
mv output/mtb-example-psoc6-uart-transmit-receive-dma.elf output/mtb-psoc6-json-parser-dma.elf
if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then docker save $tag | zstd -T0 > $filename ; fi
