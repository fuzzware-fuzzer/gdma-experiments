# T2-contiki-6lowpan
In this sample, `fuzzware genconfig` crashes when setting up a `config_autogen.yml`.
You need to setup the `config_autogen.yml` manually, which involves obtaining the memory map via `arm-none-eabi-objdump` and the symbols via `fuzzware genconfig --dump-syms`
