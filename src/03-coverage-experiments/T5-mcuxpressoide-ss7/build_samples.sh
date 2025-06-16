

out_dir="/opt/samples/output"
mod="/opt/samples/periph_uart_sg"
sample="/opt/workspace/periph_uart/Debug/periph_uart.axf"
sample_dir="/opt/workspace/periph_uart/example/src/"
new_sample="periph_uart_sg.elf"


echo "STARTING BUILDING PROCESS"

unzip -d /opt/workspace /usr/local/mcuxpressoide/ide/plugins/com.nxp.mcuxpresso.tools.wizards*/Examples/LPCOpen/lpcopen_2_19_lpcxpresso_nxp_lpcxpresso_1837.zip
cp $mod/*.h $sample_dir/
cp $mod/{isup.c,mtp2.c,mtp3.c,ss7.c,ss7_sched.c,uart.c} $sample_dir/
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -importAll /opt/workspace
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build lpc_board_nxp_lpcxpresso_1837
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build lpc_chip_18xx
/usr/local/mcuxpressoide/ide/mcuxpressoide -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /opt/workspace/ -build periph_uart/Debug

mkdir $out_dir
cp $sample $out_dir/$new_sample
echo "DONE"

