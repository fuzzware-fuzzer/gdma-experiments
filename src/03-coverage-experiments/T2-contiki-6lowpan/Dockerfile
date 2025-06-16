FROM contiker/contiki-ng:c9a0e2c8af3f6fa0feb88bb642c471fb72c2ba952f4eae404d993712d603ee44

WORKDIR /opt
RUN git clone https://github.com/contiki-ng/contiki-ng "/opt/contiki-ng"
RUN git -C "/opt/contiki-ng" checkout release/v4.9

WORKDIR /opt/contiki-ng
# Restore git state
RUN git reset --hard
RUN git clean -df
RUN git checkout release/v4.9
RUN git submodule update --init arch/cpu/nrf/lib/nrfx
RUN git submodule update --init arch/cpu/nrf/lib/tinyusb
RUN git submodule update --init arch/cpu/arm/CMSIS

# Fix CVE-2023-48229 https://github.com/contiki-ng/contiki-ng/pull/2741/commits/033d26dfc913996da24c0db3b8f36d4f7ceadb47
RUN git cherry-pick --no-commit 033d26dfc913996da24c0db3b8f36d4f7ceadb47
RUN chown -R user:user /opt
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
