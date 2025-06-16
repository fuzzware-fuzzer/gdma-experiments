# DICE Fuzzing targets evaluation
This folder contains everything to run the tool on DICE Fuzzing samples.

## `target_analysis.md`
This file contains some analysis on the DICE fuzzing targets. 
In particular, it contains information on how DICE samples use DMA, the DMA configuration, which basic blocks indicate success and references where the samples are from + if/how they are patched.

## Explanation of files in the subdirectories
For modularity, we split the fuzzware configuration files in multiples.
Each file has its dedicated purpose:
- `config_autogen.yml`: output of `fuzzware genconfig` on the target. If there are are any changes, they are indicated. Currently, none are changed.
- `config_custom.yml`: DICE binaries use a custom syscall to interact with the emulator. This configuration is not needed in fuzzware and hence the handler is replaced.
- `config.yml`: this config includes `config_autogen.yml` and `config_custom.yml`. This is the config used in the `no-dma` scenario.
- `config_generic_dma_manual.yml`: this config includes `config.yml` as well as a manually crafted configuration for the proposed DMA emulation framework. This is used in the `manual-generic-dma` scenario.
- `valid_basic_blocks.txt`: this file contains the valid basic blocks of each firmware to accurately identify basic blocks.
- `milestone_bbs.txt`: this file contains the basic blocks that indicate DMA milestones, as described in `target_analysis.md`.

## Special cases
Some test targets need special files for special situations:

### Guitar-Pedal
The guitar pedal milestone cannot be evaluated by checking for a reached basic block, as the target block is part of regular execution.
It requires coverage of a specific basic block without previously visiting another basic block.
This condition is checked in `Guitar-Pedal/check_successful_DMA.sh`.

### Soldering Station
The soldering station requires two special considerations:<br>
first, it uses a more complex state machine in DMA operations. 
Thus it is not converged yet after 24 hours. 
To rule out a fundamental problem, we investigate if it still reaches its target with additional time.
To that end, we provide mmio models discovered during previous execution to this run in order to speed up execution time.
This experiment requires two additional files: `mmio_config.yml`, which contains the mmio models discovered in previous runs, and `predefined_models.yml`, the config employed in the experiment.
This second config includes `mmio_config.yml` and `config_generic_dma_manual.yml`.
The strategy is called `manual-generic-dma-predefined`.<br>
Second, this firmware has a logic bug in the DMA setup functionality: it configures DMA with a buffer of size 20, but later operates on a buffer of size 80. 
To test both cases, this directory contains two more files: `config_dma_reference_too_large.yml` (the `reference-dma` scenario, with the larger buffer, called `reference-dma-large`) and `config_generic_dma_manual_too_large.yml` (the `manual-generic-dma` scenario, but with the larger buffer, named `manual-generic-dma-large`).
