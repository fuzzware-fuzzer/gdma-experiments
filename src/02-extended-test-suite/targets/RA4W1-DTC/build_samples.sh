/opt/e2studio/eclipse/e2studio --launcher.suppressErrors -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -consoleLog -data /work/ -importAll /opt/samples/ra4w1_serial_contiguous_dtc -cleanBuild all
mkdir -p /opt/samples/output
cp /opt/samples/ra4w1_serial_contiguous_dtc/Debug/spi_ek_ra4w1_ep.elf /opt/samples/output
