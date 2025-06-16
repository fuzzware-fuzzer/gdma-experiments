# Diverse Dataset
In this directory, we evaluate the performance of GDMA on our diverse dataset.
In particular, we want to know: Can GDMA identify and emulate all 6 types of DMA (Section 6.2)?
Does GDMA induce any false positives (Section 6.3)?

## Quick start
You need a finished fuzzing campaign (identifyable by the existence of a `results_experiment_02.yml` file in this directory).
Then run: `./eval-2.sh`

## Running the experiments
Refer to the top level for running the fuzzing campaign.

## Checking for password characters
This experiment reuses the methodology from the fuzzware paper.
We built samples for all targets that do an interative password checking on a DMA buffer.
If we find a correct password character, GDMA successfully emulated the DMA behavior.

To run the experiment, go to `scripts/` and execute `python3 cli.py eval-2`.
Use `--help` to identify optional parameters and default values.
This script checks if, for all targets, at least a single target was able to identify password characters.
The number of required password characters for successfully passing the experiment depends on the number of buffers employed by the DMA sample.
If the DMA mechanism uses a single buffer, we require at least 1 discovered character.
If the DMA mechanism uses 2 buffers, we require at least 1 discovered character per buffer.

### Expected Results
GDMA identifies identifies at least the required amount of password characters per target.

## False Positives
We manually curated a list of correct DMA configurations for all targets.
You can find these DMA configurations in the `config_generic_dma_manual.yml` files in the directory of the respective target.
In the evaluation, we check if GDMA discovered the same mechanisms that we identified manually.
If yes, the test is passed, otherwise we found a false positive.

To run the experiment, go to `scripts/` and execute `python3 cli.py eval-2-fp`.
Use `--help` to identify optional parameters and default values.

### Expected Results
We expect no false positives.
