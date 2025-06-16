target_dir="build_atmel_samples"
sample1_dir="patches"
tag="atmel-build-env"
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
cp -r $sample1_dir /tmp/$target_dir
cp build_samples.sh /tmp/$target_dir


sample_name="sam3x-x509"
sudo rm -rf /tmp/$target_dir
mkdir /tmp/$target_dir
cp -r sam3x_uart_scatter /tmp/$target_dir
cp build_samples.sh /tmp/$target_dir
if [ -e $filename ] && [ $IMPORT_IMAGES ] ; then zstd -d $filename -T0 --stdout | docker load ; else docker build . -t $tag ; fi
docker run --rm -it -v /tmp/$target_dir:/opt/samples $tag
ls /tmp/$target_dir/output
cp /tmp/$target_dir/output/sam3x_uart_scatter.elf "output/"
if [ ! -e $filename ] && [ $EXPORT_IMAGES ]; then docker save $tag | zstd -T0 > $filename ; fi
