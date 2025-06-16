#!/bin/sh

build_dir=uart2echo_LP_CC1311P3_nortos_gcc/Debug
if [ ! -d "$build_dir" ]; then
    echo "[ERROR] could not find TI project dir $build_dir"
    exit 1
fi

make -C $build_dir clean all
outdir="/opt/samples/output"
mkdir -p $outdir
elf_path=$build_dir/*.out

if [ ! -f $elf_path ]; then
	echo "[ERROR] did not find the built ELF..."
	exit 2
fi

# Copy the firmware ELF file as *.elf
fw_name=$(basename $elf_path)

echo "copying firmware $fw_name to $outdir"

cp $elf_path $outdir/${fw_name%.out}.elf
