# Dice Unit Tests
In this directory, we evaluate the performance of GDMA against DICE on DICE Unit tests.
In particular, we want to know: does GDMA perform at least as good as DICE on the DICE Unit tests (Section 6.4 in the paper)?

## Quick start
You need a finished fuzzing campaign.
Then run: `./eval-1-1.sh`

## Running the experiments
Refer to the top level for running the fuzzing campaign.

## Evaluating the results
Go to `scripts/` and execute `python3 cli.py eval-1`.
This prints an ASCII table that shows discovered models.
Use `--help` to identify optional parameters and defaults.

## Expected results
GDMA identifies DMA on all targets except for `NRF51822_console_bleprph` and `NRF52832_console_bleprph`.
In these 2 cases, the fuzzing engine does not reach the DMA part.
