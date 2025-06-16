out_dir="/opt/samples/output"
mod="/opt/samples/periph_uart"
sample="/opt/workspace/periph_uart/Debug/periph_uart.axf"
sample_dir="/opt/workspace/periph_uart/example/src/"
new_sample="periph_uart.elf"


echo "STARTING BUILDING PROCESS"

unzip -d /opt/workspace /usr/local/mcuxpressoide/ide/plugins/com.nxp.mcuxpresso.tools.wizards*/Examples/LPCOpen/lpcopen_2_19_lpcxpresso_nxp_lpcxpresso_1837.zip
cp $mod/* $sample_dir/
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -importAll /opt/workspace
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build lpc_board_nxp_lpcxpresso_1837
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build lpc_chip_18xx
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build periph_uart

mkdir $out_dir
cp $sample $out_dir/$new_sample
echo "DONE"

