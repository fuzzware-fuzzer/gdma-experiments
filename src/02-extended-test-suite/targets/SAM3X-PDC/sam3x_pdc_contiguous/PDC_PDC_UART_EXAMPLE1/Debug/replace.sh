# this assumes a valid compiler in path
sed -i "s/C:.*arm-none-eabi-gcc.exe/arm-none-eabi-gcc/g" Makefile
sed -i "s/C:.*arm-none-eabi-objcopy.exe/arm-none-eabi-objcopy/g" Makefile
sed -i "s/C:.*arm-none-eabi-objdump.exe/arm-none-eabi-objdump/g" Makefile
sed -i "s/C:.*arm-none-eabi-size.exe/arm-none-eabi-size/g" Makefile
sed -i "s/cmd.exe/\/bin\/bash/g" Makefile
