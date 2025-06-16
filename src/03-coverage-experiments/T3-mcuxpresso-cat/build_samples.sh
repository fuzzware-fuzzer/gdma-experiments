cd /opt/mcuxsdk/
cp -r /opt/samples/cat /opt
cmake -DCMAKE_TOOLCHAIN_FILE="core/tools/cmake_toolchain_files/armgcc.cmake" -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=debug /opt/cat/armgcc
make
cp /opt/cat/armgcc/debug/cat.elf /opt/samples/output

