cd /opt/samples/picohttpparser
rm -rf bluez
git clone https://github.com/bluez/bluez
cd /opt/samples/picohttpparser/bluez
git checkout 5.79
git reset --hard
cd ..
# remove tcp parsing
mv tcpip.c bluez/tools/parser/tcpip.c
# remove unused source file
rm bluez/lib/sdp.c
/opt/e2studio/eclipse/e2studio --launcher.suppressErrors -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -consoleLog -data /work/ -importAll /opt/samples/picohttpparser/ -cleanBuild all
cp Debug/spi_ek_ra4w1_ep.elf /opt/samples/output 

